from ZHU_ZIRUI_solution import ZZR_cal_average

def main():
    try:
        print(ZZR_cal_average([2, 6, 8, 3, 4, 6])) # 输出应该为4.83
    except ValueError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()