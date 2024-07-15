import random

adjectives = [
    "멋진",
    "귀여운",
    "활기찬",
    "용감한",
    "똑똑한",
    "신나는",
    "행복한",
    "슬기로운",
    "기쁜",
    "희망찬",
]

nouns = [
    "호랑이",
    "사자",
    "독수리",
    "토끼",
    "거북이",
    "고양이",
    "강아지",
    "여우",
    "늑대",
    "곰",
]


# 랜덤 한글 닉네임 생성 함수
def generate_random_korean_nickname():
    return random.choice(adjectives) + random.choice(nouns)
