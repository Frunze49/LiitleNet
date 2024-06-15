## Реализация небольшой сети офиса

1. Скачиваем обрах EVE-NG и ставим на VMware Workstation.

2. После установки и настройки, устанавливаем CISCO vIOS для роутера и коммутатора.

3. Построим систему как на рисунке. Используем 2 VPCS(клиенты), 3 Cisco vIOS Switch (Коммутаторы), 1 Cisco vIOS Router (Маршрутизатор)

   ![image](https://github.com/Frunze49/LiitleNet/assets/88929713/9716b944-6aa6-4fce-a0f0-b37e3378c8d1)

4. Настроим клиентов. Включим их, откроем терминал первого клиента, зададим ему имя, адрес (10.0.10.2) и укажем адрес шлюза (10.0.10.1):
```
set pcname Client1
ip 10.0.10.2/24 10.0.10.1
```
Аналогично, для второго клиента:
```
set pcname Client2
ip 10.0.20.2/24 10.0.20.1
```

5. Настроим коммутаторы. Включим коммутатор доступа первого клиента,
откроем терминал, назначим имя, объявим локальные сети 10 и 20, настроим связь с первым клиентом,
чтобы создать vlan 10, настроим линки со остальными двумя коммутаторами, чтобы прокидывать vlan10,20

```
enable
configure terminal
hostname AS1
vlan 10
exit
vlan 20
exit
interface gi 0/2
switchport mode access
switchport access vlan 10
exit
interface range gi 0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```
Аналогично для второго клиента, только заменим имя и vlan 10 на 20 для интерфейса gi 0/2.

Для главого коммутатора назначим имя, объявим vlan 10,20 для gi 0/0-2,
назначим его узлом корнем STP деревьев vlan 10,20

```
enable
configure terminal
hostname SS
vlan 10
exit
vlan 20
exit
interface range gi 0/0-2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
spanning-tree vlan 10 root primary
spanning-tree vlan 20 root primary
exit
write memory
```

6. Настроим роутер. Включим, дадим ему имя, включим интерфейс для главного коммутатора,
объявим два подынтерфейса для (vlan 10, 10.0.10.1/24) и (vlan20, 10.0.20.1/24).
```
enable
configure terminal
hostname Router
interface gi 0/1
no shutdown
interface gi 0/1.1
encapsulation dot1q 10
ip address 10.0.10.1 255.255.255.0
exit
interface gi 0/1.2
encapsulation dot1q 20
ip address 10.0.20.1 255.255.255.0
exit
exit
write memory
```

7. Проверим, что пинги клиентов доходят друг до друга

![image](https://github.com/Frunze49/LiitleNet/assets/88929713/5c3d87c3-f1e7-450c-a1d9-8bfdfa3b148b)

![image](https://github.com/Frunze49/LiitleNet/assets/88929713/0c635cdc-9c9d-4fb5-91fa-ff06294c55fd)

Стоит, отметить, что коммутатор уровня распределения является корнем сети для обоих VLAN, мы это прописали и можем проверить прописав на всех свичах:

```
show spanning-tree vlan 10
show spanning-tree vlan 20
```

Увидим только на главном коммутаторе:

```
The bridge is the root
```

В продолжение предыдущего пункта заметим, что на коммутаторе у второго клиента в деревьях STP как для vlan 10, так и для vlan 20 линк c коммутатором доступа первого клиента (интерфейс Gi0/1) считается альтернативным и заблокированным:

8. Проверим на отказоустойчивость. Отключим по очереди каждый из трех линков и проверим, что
9. клиенты могут пинговать друг друга.

   ![image](https://github.com/Frunze49/LiitleNet/assets/88929713/72a22eb1-26c0-4685-948e-658a72fa7f7d)

   ![image](https://github.com/Frunze49/LiitleNet/assets/88929713/a31aa101-87c8-4ebb-989d-e6efe1405473)

   ![image](https://github.com/Frunze49/LiitleNet/assets/88929713/a345b3ae-c81f-4098-ac5f-8c05a42aec97)


Везде увидим.

![image](https://github.com/Frunze49/LiitleNet/assets/88929713/2eb8c5b3-0169-41cf-b1ea-e6737aecbd96)

![image](https://github.com/Frunze49/LiitleNet/assets/88929713/2b2c59d2-f526-4134-9aa8-225f4d8797cc)

Работа в EVE-NG была выполнена