def selector(items:list, message, returnItem=False, spos=None, pre='',over='', pre2=None, over2=None):
    ok = True
    off = ''
    if not pre2:
        pre2 = pre
    if not over2:
        over2 = over
    pos = None
    if spos:
        pos = list(spos)
        off = f'\033[{pos[1]};{pos[0]*2}H'
    while ok:
        for item in items:
            print(f'{pre}{off}[{items.index(item)}] {item}{over}')
            if pos:
                pos[1]+=1
                off = f'\033[{pos[1]};{pos[0] * 2}H'

        if pos:
            pos[1] += 1
            off = f'\033[{pos[1]};{pos[0] * 2}H'
        index = input(f'{pre2}{off}Select {message} > {over2}')
        try:
            index = int(index)
            items[index]
            ok = False
        except:
            if spos:
                pos = list(spos)
    if returnItem:
        return items[index]
    return index