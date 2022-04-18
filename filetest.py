import os
import dictLevel

nickname = str(input('Ввеите ник: '))
while True:
    selectLevel = str(input('Введите уровень: '))
    if selectLevel == '1':
        prise = dictLevel.level[1]
        break
    elif selectLevel == '2':
        prise = dictLevel.level[2]
        break
    elif selectLevel == '3':
        prise = dictLevel.level[3]
        break
    else:
        print('Ошибка')

print('Ник:',nickname,'Желаемый уровень:',selectLevel)
print('Записываю в файл')

if not os.path.isdir('userdata'):
    os.mkdir('UserData')
prevDir = os.getcwd()
os.chdir('UserData')
data = open('Data.txt','w')
data.write(selectLevel +' '+ prise)
data.close()
if os.path.isfile(f'{nickname}.txt'):
    os.remove(f'{nickname}.txt')
os.rename('Data.txt',f'{nickname}.txt')
os.chdir(prevDir)