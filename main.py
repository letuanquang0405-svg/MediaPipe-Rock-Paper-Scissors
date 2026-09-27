import cv2
import mediapipe as mp
import random
import math
import time

# =========================
# MediaPipe setup
# =========================
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

# =========================
# Game state
# =========================
choices = ["ROCK", "PAPER", "SCISSORS"]
score_player = 0
score_computer = 0
score_draw = 0

player_choice = "NONE"
computer_choice = "NONE"
result = "SHOW YOUR HAND"

last_round_time = 0
round_cooldown = 1.5

# Keep the previous detected gesture to make the game less sensitive
# to one-frame detection errors.
stable_gesture = "NONE"
candidate_gesture = "NONE"
candidate_count = 0
STABLE_FRAMES = 5


def distance(a, b):
    """Euclidean distance between two MediaPipe landmarks."""
    return math.hypot(a.x - b.x, a.y - b.y)


def finger_extended(lm, tip, pip, mcp):
    """
    For the four non-thumb fingers, a finger is considered extended
    when the fingertip is farther from the wrist than the PIP joint.
    This works with the normalized hand coordinates supplied by MediaPipe.
    """
    wrist = lm[0]
    return distance(lm[tip], wrist) > distance(lm[pip], wrist)


def thumb_extended(lm):
    """
    Thumb detection based on the distance from the thumb tip to the
    wrist and thumb MCP. The extra comparison helps distinguish
    an extended thumb from a folded thumb.
    """
    wrist = lm[0]
    tip = lm[4]
    mcp = lm[2]
    return distance(tip, wrist) > distance(mcp, wrist) * 1.35


def classify_hand(lm):
    """
    Convert 21 MediaPipe hand landmarks into one of:
    ROCK / PAPER / SCISSORS / NONE.

    Our own logic:
      - Rock: 0 extended fingers
      - Paper: 4 fingers + thumb extended
      - Scissors: index + middle extended, ring + pinky folded
    """
    thumb = thumb_extended(lm)
    index = finger_extended(lm, 8, 6, 5)
    middle = finger_extended(lm, 12, 10, 9)
    ring = finger_extended(lm, 16, 14, 13)
    pinky = finger_extended(lm, 20, 18, 17)

    states = [thumb, index, middle, ring, pinky]
    count = sum(states)

    if count == 0:
        return "ROCK"

    if count == 5 or (thumb and index and middle and ring and pinky):
        return "PAPER"

    if index and middle and not ring and not pinky:
        return "SCISSORS"

    return "NONE"


def decide_winner(player, computer):
    if player == "NONE":
        return "NONE"

    if player == computer:
        return "DRAW"

    if (
        (player == "ROCK" and computer == "SCISSORS")
        or (player == "PAPER" and computer == "ROCK")
        or (player == "SCISSORS" and computer == "PAPER")
    ):
        return "PLAYER"

    return "COMPUTER"


def play_round(player):
    global score_player, score_computer, score_draw
    global player_choice, computer_choice, result, last_round_time

    computer = random.choice(choices)
    winner = decide_winner(player, computer)

    player_choice = player
    computer_choice = computer

    if winner == "PLAYER":
        score_player += 1
        result = "YOU WIN!"
    elif winner == "COMPUTER":
        score_computer += 1
        result = "COMPUTER WINS!"
    else:
        score_draw += 1
        result = "DRAW!"

    last_round_time = time.time()


def draw_text(frame, text, pos, scale=0.7, thickness=2):
    cv2.putText(
        frame,
        text,
        pos,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        (255, 255, 255),
        thickness,
        cv2.LINE_AA
    )


# =========================
# Main loop
# =========================
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise RuntimeError(
        "Cannot open camera. Please check that your webcam is available."
    )

print("Rock-Paper-Scissors started.")
print("Show ROCK / PAPER / SCISSORS to the camera.")
print("Press Q to quit, R to reset the score.")

while True:
    ok, frame = cap.read()

    if not ok:
        print("Cannot read frame from camera.")
        break

    # Mirror the camera so interaction feels natural.
    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    rgb.flags.writeable = False
    result_mp = hands.process(rgb)
    rgb.flags.writeable = True

    current_gesture = "NONE"

    if result_mp.multi_hand_landmarks:
        hand_landmarks = result_mp.multi_hand_landmarks[0]
        current_gesture = classify_hand(hand_landmarks.landmark)

        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )

    # Stability filter: require the same gesture for several frames.
    if current_gesture == candidate_gesture:
        candidate_count += 1
    else:
        candidate_gesture = current_gesture
        candidate_count = 1

    if candidate_count >= STABLE_FRAMES:
        stable_gesture = candidate_gesture

    # Start a new round when a valid gesture is held steadily.
    if (
        stable_gesture in choices
        and time.time() - last_round_time >= round_cooldown
    ):
        play_round(stable_gesture)
        stable_gesture = "NONE"
        candidate_gesture = "NONE"
        candidate_count = 0

    # =========================
    # UI
    # =========================
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (700, 180), (30, 30, 30), -1)
    frame = cv2.addWeighted(overlay, 0.75, frame, 0.25, 0)

    draw_text(frame, "MEDIA PIPE ROCK - PAPER - SCISSORS", (20, 35), 0.72, 2)
    draw_text(frame, f"Your hand: {current_gesture}", (20, 70), 0.65, 2)
    draw_text(frame, f"You: {player_choice}", (20, 105), 0.60, 2)
    draw_text(frame, f"Computer: {computer_choice}", (260, 105), 0.60, 2)
    draw_text(frame, result, (20, 145), 0.65, 2)
    draw_text(
        frame,
        f"Score  You {score_player} - {score_computer} Computer  |  Draw {score_draw}",
        (20, 175),
        0.52,
        1
    )

    draw_text(
        frame,
        "Hold a gesture for a moment | R: reset | Q: quit",
        (20, frame.shape[0] - 20),
        0.55,
        1
    )

    cv2.imshow("MediaPipe Rock-Paper-Scissors", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("r"):
        score_player = 0
        score_computer = 0
        score_draw = 0
        player_choice = "NONE"
        computer_choice = "NONE"
        result = "SHOW YOUR HAND"
        last_round_time = time.time()

cap.release()
cv2.destroyAllWindows()
hands.close()
