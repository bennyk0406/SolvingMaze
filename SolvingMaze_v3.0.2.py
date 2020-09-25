#======================#
#                      #
#       version        #
#        3.0.1         #
#                      #
#======================#


import sys
import tkinter
import copy

global a
global window
global short

short=1e10
path_result=[]
check=[]

def event(i): #지도를 만들 때 좌클릭을 하면 호출되는 함수
    global a
    if str(i)==".!button":
        name = 1
    else:
        name = int(str(i)[8:]) #버튼이 몇번째 버튼인지 설정
    if name in a:
        if len(startlist)>=1 and startlist[0][1]==(name+sizex-1)%sizex and startlist[0][0]==(name-1)//sizex:
            return
        elif len(startlist)==2 and startlist[1][1]==(name+sizex-1)%sizex and startlist[1][0]==(name-1)//sizex:
            return #클릭한 버튼이 시작점 or 도착점이라면 무시
        else:
            i.configure(background='black') #버튼 색 검정색으로 변경
            a.remove(name)
            if len(startlist)>0 and startlist[0][0]==(name+sizex-1)%sizex and startlist[0][1]==(name-1)//sizex:
                del startlist[0] #이건 걍 달지마 뭔지 모르겠음 ㄹㅇㅋㅋ
            elif len(startlist)==2 and startlist[1][0]==(name+sizex-1)%sizex and startlist[1][1]==(name-1)//sizex:
                del startlist[1]
    else:
        i.configure(background='white')
        a.append(name)

def close(a): # "결과보기" 버튼 클릭했을 때 호출되는 함수
    global window
    window.destroy()
    if len(startlist)==2:
        makemap(a) #맵을 만듬 (2차원 형태로)
    else:
        print("출발점 또는 도착점이 없어 종료합니다.") #시작점, 도착점 설정 안되어있을 시 종료
        return

def start(c):
    global a
    if str(c.widget)==".!button":
        name = 1
    else:
        name = int(str(c.widget)[8:]) #버튼이 몇 번째 버튼인지 설정
    if name in a:
        if len(startlist)>=1 and startlist[0][1]==(name+sizex-1)%sizex and startlist[0][0]==(name-1)//sizex:
            del startlist[0]
            c.widget.configure(bg='black')
            a.remove(name) #이미 시작점/도착점이었다면 취소하고 노란색으로 바꿈
        elif len(startlist)==2 and startlist[1][1]==(name+sizex-1)%sizex and startlist[1][0]==(name-1)//sizex:
            del startlist[1]
            c.widget.configure(bg='black') 
            a.remove(name) #이미 시작점/도착점이었다면 취소하고 노란색으로 바꿈
        elif len(startlist)==2:
            return #이미 시작점/도착점이 설정되어있을 때 추가하려하면 무시
        else:
            a.append(name)
            c.widget.configure(bg='yellow')
            startlist.append([(name-1)//sizex, (name+sizex-1)%sizex]) #시작점 or 도착점으로 추가
    else:
        if len(startlist)==2:
            return 
        a.append(name)
        c.widget.configure(bg='yellow')
        startlist.append([(name-1)//sizex, (name+sizex-1)%sizex]) #시작점 or 도착점으로 추가

def isPath(Map,check,x,y): #길을 찾을 때 쓰이는 함수, 가려는 경로가 길인지 벽인지 알려줌
    if Map[y][x]!=0 or check[y][x]==True:
        return False
    return True

def isValid(x,y): #길을 찾을 때 쓰이는 함수, 가려는 경로가 맵 안에 있는지 알려줌
    if x<sizex and y<sizey and x>=0 and y>=0:
        return True
    return False

def solve(Map, check, x, y, cur_dist, short_dist, short_path, cur_path): #길을 찾음
    global startlist
    global path_result
    global short
    if y==startlist[1][0] and x==startlist[1][1]: #도착했다면
        if cur_dist < short: #현재의 경로 길이가 이전의 최소 길이보다 작다면
            short_dist = cur_dist
            short_path.clear()
            short_path.extend(cur_path)
            short_path.append([startlist[1][0], startlist[1][1]])
            short=short_dist
            path_result=short_path #현재의 경로를 최단 경로로 재설정
        return
    check[y][x]=True #지금 위치해있는 곳을 방문 리스트에 넣음
    cur_path.append([y,x])
    if isValid(x+1, y) and isPath(Map, check ,x+1, y):
        solve(Map, check, x+1, y, cur_dist+1, short_dist, short_path, cur_path)
    if isValid(x, y+1) and isPath(Map, check, x, y+1):
        solve(Map, check, x, y+1, cur_dist+1, short_dist, short_path, cur_path)
    if isValid(x-1, y) and isPath(Map, check, x-1, y):
        solve(Map, check, x-1, y, cur_dist+1, short_dist, short_path, cur_path)
    if isValid(x, y-1) and isPath(Map, check, x, y-1):
        solve(Map, check, x, y-1, cur_dist+1, short_dist, short_path, cur_path) #상,하,좌,우를 탐색함
    check[y][x] = False 
    cur_path.pop() 

def makemap(a): #버튼 리스트를 2차원 맵으로 바꿔주는 함수
    Map=[]
    a.sort()
    for j in range(sizey):
        Map.append([])
    for i in range(sizex*sizey):
        if (i+1) in a:
            Map[i//sizex].append(0) #길은 0
        else:
            Map[i//sizex].append(1) #벽은 1
    showresult(Map)
    return Map
    
def showresult(Map): #결과를 보여주는 함수
    global path_result
    sys.setrecursionlimit(1000000)
    solve(Map, check, startlist[0][1], startlist[0][0], 0, short_dist, short_path, cur_path) #시작점부터 출발
    if path_result!=[]: #최단경로가 있다면
        print("Yes") 
        window_result = tkinter.Tk()
        window_result.title('RESULT')
        window_result.attributes('-fullscreen', True)
        pixel=tkinter.PhotoImage(width=1, height=1)
        for i in path_result:
            Map[i[0]][i[1]]=2    
        Map[startlist[0][0]][startlist[0][1]]=3
        Map[startlist[1][0]][startlist[1][1]]=3
        for i in range(sizex): #길은 하양, 벽은 검정, 경로는 분홍, 시작/도착점은 노랑으로 나오게함
            for j in range(sizey):
                if Map[j][i]==0:
                    tkinter.Button(window_result, text="", image=pixel, width=button_size, height=button_size, compound='c', bg='white').place(x=10+button_size*i, y=10+button_size*j)
                if Map[j][i]==1:
                    tkinter.Button(window_result, text="", image=pixel, width=button_size, height=button_size, compound='c', bg='black').place(x=10+button_size*i, y=10+button_size*j)
                if Map[j][i]==2:
                    tkinter.Button(window_result, text="", image=pixel, width=button_size, height=button_size, compound='c', bg='pink').place(x=10+button_size*i, y=10+button_size*j)          
                if Map[j][i]==3:
                    tkinter.Button(window_result, text="", image=pixel, width=button_size, height=button_size, compound='c', bg='yellow').place(x=10+button_size*i, y=10+button_size*j)
        tkinter.Button(window_result, text="종료하기", command=lambda:window_result.destroy()).place(x=10, y=20+button_size*sizey)
    else:
        print("No")

a=[]
startlist=[]

if __name__=='__main__': #프로그램 시작
    short_dist=1e11
    short_path=[]
    cur_path=[]
    sizex=int(input('미로의 가로 사이즈를 정해주세요. : '))
    sizey=int(input('미로의 세로 사이즈를 정해주세요. : '))
    if sizey>=15:
        button_size=780/sizey
    else:
        button_size=50
    if button_size*sizex>=1500:
        button_size=1500/sizex #미로 사이즈에 맞는 버튼 크기 설정
    window=tkinter.Tk()
    window.title('miro')
    window.attributes('-fullscreen', True)
    pixelVirtual=tkinter.PhotoImage(width=1, height=1)
    for i in range(sizey): #방문 리스트 생성
        check.append([])
        for j in range(sizex):
            check[i].append(False) 
    for i in range(sizex*sizey): #입력할 미로 틀 생성
        button = tkinter.Button(window, text="", image=pixelVirtual, width=button_size, height=button_size, compound='c', bg='black')
        button.place(x=10+button_size*(i%sizex), y=10+button_size*(i//sizex))
        button.configure(command=lambda b=button:event(b))
        button.bind("<Button-3>", start)
    tkinter.Button(window, text="결과보기", command=lambda:close(a)).place(x=10, y=sizey*button_size+20) #결과보기 버튼
