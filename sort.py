def term(tn):
    match tn:
        case '1':
            return '九年级上学期'
        case '2':
            return '九年级下学期'
        case '3':
            return '十年级上学期'
        case '4':
            return '十年级下学期'
        case '5':
            return '十一年级上学期'
        case '6':
            return '十一年级下学期'
        case '7':
            return '十二年级上学期'
        case '8':
            return '十二年级下学期'
        case _:
            return '未知学期'
        

        
def sort(FID,fileLoca):
    try:
        details = FID.split('-')
        print(details)
        loca = fileLoca+'\\'
        print(details[0])
        match details[0]:
            case 'ZH':
                loca+='语文\\'
                match details[1]:
                    case 'CG':
                        loca+='常规作业\\'
                        match details[2]:
                            case '1':
                                loca+='随笔\\{}\\第{}期（第{}页）.jpg'.format(term(details[3]),details[4],details[5])
                            case '2':
                                loca+='成语\\{}\\第{}期（第{}页）.jpg'.format(term(details[3]),details[4],details[5])
                            case '3':
                                loca+='摘记\\{}\\第{}期（第{}页）.jpg'.format(term(details[3]),details[4],details[5])
                            case '4':
                                loca+='摘记材料\\{}\\第{}期（第{}页）.jpg'.format(term(details[3]),details[4],details[5])
                    case 'WY':
                        loca+='文言知识积累\\第{}册语文书\\课文{}（第{}页）.jpg'.format(details[2],details[3],details[4])
                    case 'DT':
                        loca+='典题整理\\20{}年{}月{}日考试典题（第{}页）.jpg'.format(details[2],details[3],details[4],details[5])
                    case 'WS':
                        loca+='任务单\\第{}册语文书\\课文{}(第{}页).jpg'.format(details[2],details[3],details[4])
            case 'MAT':
                loca+='数学\\'
                match details[1]:
                    case 'ZC':
                        loca+='周测\\{}\\{}(第{}页).jpg'.format(term(details[2]),details[3],details[4])
                    case 'CT':
                        loca+='错题\\{}\\{}月{}日（第{}页）.jpg'.format(term(details[2]),details[3],details[4],details[5])
                    case 'WS':
                        loca+='任务单\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'BJ':
                        loca+='笔记\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
            case 'ENG':
                loca+='英语\\'
                match details[1]:
                    case 'CG':
                        loca+='常规阅读\\{}\\第{}页.jpg'.format(term(details[2]),details[3])
                    case 'DC':
                        loca+='单词积累\\{}第{}页.jpg'.format(term(details[2]),details[3])
                    case 'BJ':
                        loca+='笔记\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
            case 'PHYGK':
                loca+='高考物理\\'
                match details[1]:
                    case 'CT':
                        loca+='错题\\{}\\{}月{}日（第{}页）.jpg'.format(term(details[2]),details[3],details[4],details[5])
                    case 'WS':
                        loca+='任务单\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'BJ':
                        loca+='笔记\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
            case 'PHYSNR':
                loca+='竞赛物理\\'
                match details[1]:
                    case 'DT':
                        loca+='典题\\{}（第{}页）.jpg'.format(details[2],details[3])
                    case 'WS':
                        loca+='任务单\\{}（第{}页）.jpg'.format(details[2],details[3])
                    case 'BJ':
                        loca+='笔记\\{}（第{}页）.jpg'.format(details[2],details[3])
            case 'BIO':
                loca+='生物\\'
                match details[1]:
                    case 'CT':
                        loca+='错题\\{}\\{}月{}日（第{}页）.jpg'.format(term(details[2]),details[3],details[4],details[5])
                    case 'WS':
                        loca+='任务单\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'BJ':
                        loca+='笔记\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'XTC':
                        loca+='习题册\\{}\\{}第{}页.jpg'.format(term(details[2]),details[3],details[4])
            case 'CEM':
                loca+='化学\\'
                match details[1]:
                    case 'CT':
                        loca+='错题\\{}\\{}月{}日（第{}页）.jpg'.format(term(details[2]),details[3],details[4],details[5])
                    case 'WS':
                        loca+='任务单\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'BJ':
                        loca+='笔记\\{}\\{}（第{}页）.jpg'.format(term(details[2]),details[3],details[4])
                    case 'XTC':
                        loca+='习题册\\{}\\{}第{}页.jpg'.format(term(details[2]),details[3],details[4])
            case 'TS':
                loca+='考试\\{}\\'.format(term(details[1]))
                match details[2]:
                    case '1':
                        loca+='开学考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答题卡（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答案（第{}页）.jpg'.format(details[5])
                    case '2':
                        loca+='第一次月考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答题卡（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答案（第{}页）.jpg'.format(details[5])
                    case '3':
                        loca+='期中考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答题卡（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答案（第{}页）.jpg'.format(details[5])
                    case '4':
                        loca+='第二次月考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答题卡（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答案（第{}页）.jpg'.format(details[5])
                    case '5':
                        loca+='期末考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答题卡（第{}页）.jpg'.format(details[5])
                            case '1':
                                loca+='答案（第{}页）.jpg'.format(details[5])
                    case '6':
                        loca+='单元考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子{}（第{}页）.jpg'.format(details[5],details[6])
                            case '2':
                                loca+='答题卡{}（第{}页）.jpg'.format(details[5],details[6])
                            case '3':
                                loca+='答案{}（第{}页）.jpg'.format(details[5],details[6])
                    case '7':
                        loca+='模拟考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子{}（第{}页）.jpg'.format(details[5],details[6])
                            case '2':
                                loca+='答题卡{}（第{}页）.jpg'.format(details[5],details[6])
                            case '3':
                                loca+='答案{}（第{}页）.jpg'.format(details[5],details[6])
                    case '8':
                        loca+='统考\\'
                        match details[3]:
                            case 'ZH':
                                loca+='语文\\'
                            case 'MAT':
                                loca+='数学\\'
                            case 'ENG':
                                loca+='英语\\'
                            case 'PHY':
                                loca+='物理\\'
                            case 'CEM':
                                loca+='化学\\'
                            case 'BIO':
                                loca+='生物\\'
                        match details[4]:
                            case '1':
                                loca+='卷子{}（第{}页）.jpg'.format(details[5],details[6])
                            case '2':
                                loca+='答题卡{}（第{}页）.jpg'.format(details[5],details[6])
                            case '3':
                                loca+='答案{}（第{}页）.jpg'.format(details[5],details[6])
            case 'OTR':
                return loca.join('其他\\{}.jpg'.fotmat(FID))
        print(loca)
        return loca
    except:
        loca = '{}\\错误的FID\\{}.jpg'.format(fileLoca,FID)
        return loca