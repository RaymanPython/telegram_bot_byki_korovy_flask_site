class Game_board:

    @staticmethod
    def prov(s, n):

        s = str(s)
        for i in s:
            if i not in map(str, range(10)):
                return False
        if len(s) != n:
            print(2)
            return False
        if len(set(list(s))) != n:
            print(3)
            return False
        if '0' == s[0]:
            print(45)
            return False
        return True

    class Answer:

        def __init__(self, b_count=0, k_count=0):
            self.b_count = b_count
            self.k_count = k_count

        def __str__(self):
            return f'быков:{self.b_count};коров:{self.k_count}'

    @staticmethod
    def count(a, b):
        b_count = 0
        k_count = 0
        for i in range(len(a)):
            if a[i] == b[i]:
                b_count += 1
            elif a[i] in b:
                k_count += 1
        return Game_board.Answer(b_count, k_count)
