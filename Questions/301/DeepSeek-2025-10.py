#### DeepSeek'in loop a girdiği bir örnek:
#### https://chat.deepseek.com/a/chat/s/82420987-8cd2-4562-bcac-a2ffe701951f

def main():
    n = 32
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    print(a)

if __name__ == '__main__':
    main()