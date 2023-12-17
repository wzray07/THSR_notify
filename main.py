from pyfiglet import Figlet
import data

def main():
    f = Figlet()
    print(f.renderText('THSR-Notify'))
    print("\n歡迎使用高鐵查票自動通知系統 \nAuthor: wzray07 \n")
    print("使用前請詳閱相關文件 \n")
    flag = True
    while(flag):
        print("請選擇操作：\n(1) 新增查詢條件 \n(2) 檢視、刪除目前查詢條件 \n(3) 退出\n")
        choice = int(input("請選擇："))
        match choice:
            case 1:
                # new
                data.new_data()
            case 2:
                # view
                data.view_data()
                print("\n請選擇下一步：")
                print("(1) 刪除 \n(2) 回到上一步 \n")
                choice_v = int(input("請選擇："))
                match choice_v:
                    case 1:
                        # delete
                        item = int(input("請輸入要刪除的號碼："))
                        data.delete_data(item)
                    case 2:
                        print("回到上一步\n")
                        continue
                    case _:
                        print("無此選項，退回上一步")
                        continue
            case 3:
                flag = False
                print("\nSee you next time~")
                # exit
            case _:
                print("無此選項，請重新選擇\n")
    

if __name__ == '__main__':
    main()