def term(tn):
    match tn:
        case "1":
            return "九年级上学期"
        case "2":
            return "九年级下学期"
        case "3":
            return "十年级上学期"
        case "4":
            return "十年级下学期"
        case "5":
            return "十一年级上学期"
        case "6":
            return "十一年级下学期"
        case "7":
            return "十二年级上学期"
        case "8":
            return "十二年级下学期"
        case _:
            return "未知学期"
        

        
def sort(FID,fileLoca):
    try:
        details = FID.split('-')
        loca = fileLoca+'\\'
        match details[0]:
            case "ZH":
                loca.join("语文\\")
                match details[1]:
                    case "CG":
                        loca.join("常规作业\\")
                        match details[2]:
                            case "1":
                                loca.join("随笔\\{}\\第{}期（第{}页）.jpg").format(term(details[3]),details[4],details[5])
                            case "2":
                                loca.join("成语\\{}\\第{}期（第{}页）.jpg").format(term(details[3]),details[4],details[5])
                            case "3":
                                loca.join("摘记\\{}\\第{}期（第{}页）.jpg").format(term(details[3]),details[4],details[5])
                    case "WY":
                        loca.join("文言知识积累\\第{}册语文书\\课文{}（第{}页）.jpg").format(details[2],details[3],details[4])
                    case "DT":
                        loca.join("典题整理\\20{}年{}月{}日考试典题（第{}页）.jpg").format(details[2],details[3],details[4],details[5])
                    case "WS":
                        loca.join("任务单\\{}\\课文{}(第{}页).jpg").format(details[2],details[3],details[4])
            case "MAT":
                loca.join("数学\\")
                match details[1]:
                    case "ZC":
                        loca.join("周测\\{}\\{}(第{}页).jpg".format(term(details[2]),details[3],details[4]))
                    case "CT":
                        loca.join("错题\\{}\\{}月{}日（第{}页）.jpg".format(term(details[2]),details[3],details[4],details[5]))
                    case "WS":
                        loca.join("任务单\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "BJ":
                        loca.join("笔记\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
            case "ENG":
                loca.join("英语\\")
                match details[1]:
                    case "CG":
                        loca.join("常规阅读\\{}\\第{}页.jpg".format(term(details[2]),details[3]))
                    case "DC":
                        loca.join("单词积累\\{}第{}页.jpg".format(term(details[2]),details[3]))
                    case "BJ":
                        loca.join("笔记\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
            case "PHYGK":
                loca.join("高考物理\\")
                match details[1]:
                    case "CT":
                        loca.join("错题\\{}\\{}月{}日（第{}页）.jpg".format(term(details[2]),details[3],details[4],details[5]))
                    case "WS":
                        loca.join("任务单\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "BJ":
                        loca.join("笔记\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
            case "PHYSNR":
                loca.join("竞赛物理\\")
                match details[1]:
                    case "DT":
                        loca.join("典题\\{}（第{}页）.jpg".format(details[2],details[3]))
                    case "WS":
                        loca.join("任务单\\{}（第{}页）.jpg".format(details[2],details[3]))
                    case "BJ":
                        loca.join("笔记\\{}（第{}页）.jpg".format(details[2],details[3]))
            case "BIO":
                loca.join("生物\\")
                match details[1]:
                    case "CT":
                        loca.join("错题\\{}\\{}月{}日（第{}页）.jpg".format(term(details[2]),details[3],details[4],details[5]))
                    case "WS":
                        loca.join("任务单\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "BJ":
                        loca.join("笔记\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "XTC":
                        loca.join("习题册\\{}\\{}第{}页.jpg".format(term(details[2]),details[3],details[4]))
            case "CEM":
                loca.join("化学\\")
                match details[1]:
                    case "CT":
                        loca.join("错题\\{}\\{}月{}日（第{}页）.jpg".format(term(details[2]),details[3],details[4],details[5]))
                    case "WS":
                        loca.join("任务单\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "BJ":
                        loca.join("笔记\\{}\\{}（第{}页）.jpg".format(term(details[2]),details[3],details[4]))
                    case "XTC":
                        loca.join("习题册\\{}\\{}第{}页.jpg".format(term(details[2]),details[3],details[4]))
            case "TS":
                loca.join("考试\\{}\\".format(term(details[1])))
                match details[2]:
                    case "1":
                        loca.join("开学考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答题卡（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答案（第{}页）.jpg".format(details[5]))
                    case "2":
                        loca.join("第一次月考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答题卡（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答案（第{}页）.jpg".format(details[5]))
                    case "3":
                        loca.join("期中考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答题卡（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答案（第{}页）.jpg".format(details[5]))
                    case "4":
                        loca.join("第二次月考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答题卡（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答案（第{}页）.jpg".format(details[5]))
                    case "5":
                        loca.join("期末考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答题卡（第{}页）.jpg".format(details[5]))
                            case "1":
                                loca.join("答案（第{}页）.jpg".format(details[5]))
                    case "6":
                        loca.join("单元考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子{}（第{}页）.jpg".format(details[5],details[6]))
                            case "2":
                                loca.join("答题卡{}（第{}页）.jpg".format(details[5],details[6]))
                            case "3":
                                loca.join("答案{}（第{}页）.jpg".format(details[5],details[6]))
                    case "7":
                        loca.join("模拟考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子{}（第{}页）.jpg".format(details[5],details[6]))
                            case "2":
                                loca.join("答题卡{}（第{}页）.jpg".format(details[5],details[6]))
                            case "3":
                                loca.join("答案{}（第{}页）.jpg".format(details[5],details[6]))
                    case "8":
                        loca.join("统考\\")
                        match details[3]:
                            case "ZH":
                                loca.join("语文\\")
                            case "MAT":
                                loca.join("数学\\")
                            case "ENG":
                                loca.join("英语\\")
                            case "PHY":
                                loca.join("物理\\")
                            case "CEM":
                                loca.join("化学\\")
                            case "BIO":
                                loca.join("生物\\")
                        match details[4]:
                            case "1":
                                loca.join("卷子{}（第{}页）.jpg".format(details[5],details[6]))
                            case "2":
                                loca.join("答题卡{}（第{}页）.jpg".format(details[5],details[6]))
                            case "3":
                                loca.join("答案{}（第{}页）.jpg".format(details[5],details[6]))
            case "OTR":
                return loca.join("其他\\{}.jpg".fotmat(FID))
        return loca
    except:
        loca = "{}\\错误的FID\\{}.jpg".format(fileLoca,FID)
        return loca