import math
# from matplotlib import pyplot as plt
import pylab 
import InteractiveSerengetiProgram as pro


def calAB():
    a1 = [1.48, 0.16]
    a2 = [1.78, 0.41]
    a3 = [2.08, 0.67]
    a4 = [2.38, 0.93]
    a5 = [2.68, 1.18]

    def getAB(e1, e2):
        M1 = math.pow(10, e1[0])
        M2 = math.pow(10, e2[0])
        T1 = math.pow(10, e1[1])
        T2 = math.pow(10, e2[1])
        b = math.log(T1 / T2, M1 / M2)
        a = T1 / M1
        return (T1 / math.pow(M1, b), b)

    arr = []
    arr.append(getAB(a1, a2))
    arr.append(getAB(a1, a3))
    arr.append(getAB(a1, a4))
    arr.append(getAB(a1, a5))

    arr.append(getAB(a2, a3))
    arr.append(getAB(a2, a4))
    arr.append(getAB(a2, a5))

    arr.append(getAB(a3, a4))
    arr.append(getAB(a3, a5))

    arr.append(getAB(a4, a5))
    # print(arr)

    # plt.title("Matplotlib demo")
    # plt.xlabel("x axis caption")
    # plt.ylabel("y axis caption")
    # for k, v in arr:
    #     plt.scatter(k, v)
    # plt.show()


def testTts():
    def _convert(log10M):
        m = math.pow(10, log10M)
        t = pro.time_to_top_speed(m)
        return math.log10(t)

    print(_convert(1.48))
    print(_convert(1.78))
    print(_convert(2.08))
    print(_convert(2.38))
    print(_convert(2.68))

def testTts2():
    x = range(10, 1000, 1)
    y = []
    for i in x: 
        y.append(pro.MRS_mammal(i)) 

    fig, ax = pylab.subplots()
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.05, 0.95, "textstr", transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)
    pylab.title("MRS")
    pylab.xlabel("mass(kg)")
    pylab.ylabel("MRS(km/h)")
    pylab.plot(x, y)
    pylab.legend()
    # pylab.ylim(50, 55)

    pylab.show()

def testSpeed():
    def _test1(v):
        print(pro.speed_of_predator(1, 1, v))
    _test1(0.7)
    _test1(3.5)
    _test1(5)
    _test1(8)
    print("--------------")

    def _test2(v):
        print(pro.speed_of_prey(1, 1, v))
    _test2(0.7)
    _test2(3.5)
    _test2(7)
    _test2(9)


def testChase():
    predator_mass = 140
    prey_mass = 30
    distance = 100

    resultDic = pro.chase_result(predator_mass, prey_mass, distance)
    pylab.gca().set_position((.1, .3, .8, .6)) # to make a bit of room for extra text

    pylab.title("Chasing Model")
    pylab.xlabel("time(s)" )
    pylab.ylabel("distance between predator and prey(m)")
    x = resultDic["times"]
    pylab.plot(x, resultDic["distances"], label='distances')
    pylab.plot(x, resultDic["predator_position"], label='predator')
    pylab.plot(x, resultDic["prey_position"], label='prey')
    pylab.legend()
    # pylab.figtext(.95, .9, "max_chase_time: " + str(resultDic["max_chase_time"]) , rotation='vertical')
    text = "max_chase_time: " + str(resultDic["max_chase_time"]) 
    text += "\n"
    text += "predator_mass: " + str(pro.MRS_mammal(predator_mass)) + " tts:" + str(pro.time_to_top_speed(predator_mass))
    text += "\n"
    text += "pery_mass: " + str(pro.MRS_mammal(prey_mass)) + " tts:" + str(pro.time_to_top_speed(prey_mass))
    text += "\n"
    if resultDic["is_caught_prey"] :
        text += "caught"
    else:
        text += "not caught"
    pylab.figtext(.02, .02, text)
 
    pylab.show()


def testInput():
    num = pro.get_digit_input()
    print("get num: " + str(num))

def test():
    # testTts()
    # testSpeed()
    # testChase()
    # testInput()
    testTts2()

test()

# 再看下流程图
# 检查图是否正确
# 判断逻辑
# 坐标轴名字，限定负数
# 是否要从函数拿出来放到main里