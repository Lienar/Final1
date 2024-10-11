from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import *
from random import randint

# Create your views here.
def Enter_page(request):
    Players = Player.objects.all()
    if request.method == 'POST':
        run_len = int(request.POST.get('run_len'))
        if run_len < 7:
            run_len = 7
        if run_len > 20:
            run_len = 20
        Map_len.objects.all().update(map_len=run_len)
        name = request.POST.get('name')
        for player in Players:
            if player.name == name:
                context = {'name': name}
                url_temp = f'http://127.0.0.1:8000/Player/?player_name={name}'
                return redirect(url_temp)
        return render(request, 'Create_player.html')
    return render(request, 'Enter.html')

def Create_player_page(request):
    Players = Player.objects.all()
    info = {'error': ' '}
    if request.method == 'POST':
        name = request.POST.get('name')
        for player in Players:
            if player.name == name:
                info['error'] = 'Игрок уже существует'
                return render(request, 'Create_player.html', info)

        damage = int(request.POST.get('damage'))
        if damage > 3:
            info['error'] = 'Урон не может быть больше 3'
            return render(request, 'Create_player.html', info)
        if damage < 0:
            info['error'] = 'Урон не может быть меньше 0'
            return render(request, 'Create_player.html', info)
        player_attack1_name = request.POST.get('player_attack1_name')
        player_attack2_name = request.POST.get('player_attack2_name')
        Player.objects.create(name=name, damage_max=damage, damage_min=1, health=10, player_attack1_name=player_attack1_name,
                              player_attack2_name=player_attack2_name, player_attack1_damage_max=damage,
                              player_attack1_damage_min=1, player_attack2_damage_max=damage*2, player_attack2_damage_min=2,
                              player_attack1_cooldown=1, player_attack2_cooldown=randint(1,5))
        return render(request, 'Player.html', )
    return render(request, 'Create_player.html')

def Player_page(request):
    name = request.GET.get('player_name', 'Vasya')
    player = Player.objects.get(name=name)
    context = {'player_name': player.name, 'health': player.health,
               'player_attack1_name': player.player_attack1_name, 'player_attack2_name': player.player_attack2_name,
               'player_attack1_damage_min': player.player_attack1_damage_min, 'player_attack1_damage_max': player.player_attack1_damage_max,
               'player_attack2_damage_min': player.player_attack2_damage_min, 'player_attack2_damage_max': player.player_attack2_damage_max,
               'player_attack1_cooldown': player.player_attack1_cooldown, 'player_attack2_cooldown': player.player_attack2_cooldown,}
    return render(request, 'Player.html', context)

def Move_request(request):
    player_name = request.GET.get('player_name', 'Player')
    location_map_id = int(request.GET.get('location_map_id', '1'))
    run_end_location = Map_len.objects.get(id=1)
    if location_map_id == run_end_location.map_len:
        url_temp = f'http://127.0.0.1:8000/Winning_page/?player_name={player_name}'
        return redirect(url_temp)
    location_map_id += 1
    map_temp = Map.objects.get(id_number=location_map_id)
    if (map_temp.is_it_enemy == False):
        next_location_id = map_temp.location_id
        url_temp = f'http://127.0.0.1:8000/Location/?player_name={player_name}&location_id={next_location_id}&location_map_id={location_map_id}'
        return redirect(url_temp)
    else:
        next_enemy_id = map_temp.enemy_class
        enemy_name = Enemy.objects.get(enemy_class=next_enemy_id).name
        url_temp = f'http://127.0.0.1:8000/Battel/?player_name={player_name}&enemy_name={enemy_name}&location_map_id={location_map_id}'
        return redirect(url_temp)

def Enemy_page(request):
    player_name = request.GET.get('player_name', 'Player')
    enemy_name = request.GET.get('enemy_name', '1')
    location_map_id = int(request.GET.get('location_map_id', '3'))
    player = Player.objects.get(name=player_name)
    turn = int(request.GET.get('turn', '0'))
    enemy = Enemy.objects.get(name=enemy_name)
    player_attack = request.GET.get('player_attack_name', player.player_attack1_name)
    player_health = int(request.GET.get('player_health', player.health))
    enemy_health = int(request.GET.get('enemy_health', enemy.health))
    player_attack1_cooldown = int(request.GET.get('player_attack1_cooldown', player.player_attack1_cooldown))
    player_attack2_cooldown = int(request.GET.get('player_attack2_cooldown', player.player_attack2_cooldown))
    enemy_attack1_cooldown = int(request.GET.get('player_attack1_cooldown', enemy.enemy_attack1_cooldown))
    enemy_attack2_cooldown = int(request.GET.get('player_attack2_cooldown', enemy.enemy_attack2_cooldown))
    is_player_win = False
    enemy_text = f'{enemy.name} напал на {player_name}'
    player_text = f'{player_name} думает, что сделать'
    cooldown1 = player.player_attack1_cooldown - player_attack1_cooldown
    cooldown2 = player.player_attack2_cooldown - player_attack2_cooldown
    if turn != 1:
        player_damage = randint(player.player_attack1_damage_min, player.player_attack1_damage_max + 1)
        if player.player_attack1_name == player_attack and player.player_attack1_cooldown - player_attack1_cooldown > 0:
            player_damage = 0
        if player.player_attack2_name == player_attack and player.player_attack2_cooldown - player_attack2_cooldown > 0:
            player_damage = 0
        if player.player_attack1_name == player_attack and player.player_attack1_cooldown - player_attack1_cooldown < 0:
            player_attack1_cooldown = 0
        if player.player_attack2_name == player_attack and player.player_attack2_cooldown - player_attack2_cooldown < 0:
            player_attack2_cooldown = 0
        player_attack1_cooldown += 1
        player_attack2_cooldown += 1
        player_text = f'{player_name} ударил на {player_damage}'
        is_player_win = False
        enemy_attack = 0
        if enemy_health - player_damage > 0:
            enemy_health = enemy_health - player_damage
            print(enemy.enemy_attack2_cooldown - enemy_attack2_cooldown)
            print(enemy.enemy_attack1_cooldown - enemy_attack1_cooldown)
            if enemy.enemy_attack2_cooldown - enemy_attack2_cooldown < 0 and enemy.enemy_attack1_cooldown - enemy_attack1_cooldown < 0:
                if randint(0, 2) == 0:
                    enemy_attack = randint(enemy.enemy_attack1_damage_min, enemy.enemy_attack1_damage_max + 1)
                    enemy_attack1_cooldown = 0
                else:
                    enemy_attack = randint(enemy.enemy_attack2_damage_min, enemy.enemy_attack2_damage_max + 1)
                    enemy_attack2_cooldown = 0
            if enemy.enemy_attack2_cooldown - enemy_attack2_cooldown > 0:
                enemy_attack = randint(enemy.enemy_attack1_damage_min, enemy.enemy_attack1_damage_max + 1)
                enemy_attack1_cooldown = 0
            if enemy.enemy_attack1_cooldown - enemy_attack1_cooldown > 0:
                enemy_attack = randint(enemy.enemy_attack2_damage_min, enemy.enemy_attack2_damage_max + 1)
                enemy_attack2_cooldown = 0
            enemy_attack1_cooldown += 1
            enemy_attack2_cooldown += 1
            enemy_text = f'{enemy.name} ударил на {enemy_attack}'
            is_player_win = False
            if player_health - enemy_attack > 0:
                player_health = player_health - enemy_attack
                context = {'player_name': player_name, 'player_health': player_health,
                           'player_attack1_name': player.player_attack1_name, 'player_damage': player_damage,
                           'player_attack2_name': player.player_attack2_name, 'enemy_name': enemy.name,
                           'player_attack1_damage_max': player.player_attack1_damage_max,
                           'player_attack1_damage_min': player.player_attack1_damage_min,
                           'player_attack2_damage_minx': player.player_attack2_damage_min,
                           'player_attack2_damage_max': player.player_attack2_damage_max,
                           'player_attack1_cooldown': player_attack1_cooldown,
                           'player_attack2_cooldown': player_attack2_cooldown,
                           'cooldown1': cooldown1, 'cooldown2': cooldown2,
                           'is_player_win': is_player_win, 'enemy_health': enemy_health,
                           'enemy_attack1_cooldown': enemy_attack1_cooldown,
                           'enemy_attack2_cooldown': enemy_attack2_cooldown, 'turn': turn,
                           'enemy_text': enemy_text, 'player_text': player_text, 'location_map_id': location_map_id}
            else:
                contex = {'player_name': player_name, 'reason_name': enemy.name,
                          'text': f'Игрок {player_name}, не смог победить даже {enemy.name}'}
                return render(request, 'Gameover.html', contex)
            return render(request, 'Battel.html', context)
        player_text = f'{player_name} победил'
        if enemy_health - player_damage <= 0:
            enemy_health = enemy_health - player_damage
            enemy_text = f'{enemy.name} пал'
            is_player_win = True
            context = {'player_name': player_name, 'player_health': player_health,
                       'player_damage': player_damage,
                       'is_player_win': is_player_win, 'enemy_name': enemy.name,
                       'player_attack1_name': player.player_attack1_name,
                       'player_attack2_name': player.player_attack2_name,
                       'player_attack1_damage_max': player.player_attack1_damage_max,
                       'player_attack1_damage_min': player.player_attack1_damage_min,
                       'player_attack2_damage_min': player.player_attack2_damage_min,
                       'player_attack2_damage_max': player.player_attack2_damage_max,
                       'player_attack1_cooldown': player_attack1_cooldown,
                       'player_attack2_cooldown': player_attack2_cooldown,
                       'cooldown1': cooldown1, 'cooldown2': cooldown2,
                       'enemy_health': enemy_health, 'location_map_id': location_map_id,
                       'enemy_attack1_cooldown': enemy_attack1_cooldown,
                       'enemy_attack2_cooldown': enemy_attack2_cooldown, 'turn': turn,
                       'enemy_text': enemy_text, 'player_text': player_text, }
            return render(request, 'Battel.html', context)
    if player_damage <= 0:
        player_damage = 0
    context = {'player_name': player_name, 'player_health': player_health,
               'player_damage': player_damage,
               'is_player_win': is_player_win, 'enemy_name': enemy.name,
               'player_attack1_name': player.player_attack1_name,
               'player_attack2_name': player.player_attack2_name,
               'player_attack1_damage_max': player.player_attack1_damage_max,
               'player_attack1_damage_min': player.player_attack1_damage_min,
               'player_attack2_damage_min': player.player_attack2_damage_min,
               'player_attack2_damage_max': player.player_attack2_damage_max,
               'player_attack1_cooldown': player_attack1_cooldown,
               'player_attack2_cooldown': player_attack2_cooldown,
               'cooldown1': cooldown1, 'cooldown2': cooldown2,
               'enemy_health': enemy_health, 'location_map_id': location_map_id,
               'enemy_attack1_cooldown': enemy_attack1_cooldown,
               'enemy_attack2_cooldown': enemy_attack2_cooldown, 'turn': turn,
               'enemy_text': enemy_text, 'player_text': player_text, }
    return render(request, 'Battel.html', context)

def Location_page(request):
    player_name = request.GET.get('player_name', 'Player')
    location_map_id = request.GET.get('location_map_id', '1')
    this_location_id = request.GET.get('location_id', '1')
    location = Location.objects.get(id_number=this_location_id)
    if randint(0, 11) < 5 and location.trap_exists == True:
        this_player_health = Player.objects.get(name=player_name).health
        trap_damage = randint(location.trap_damage_min, location.trap_damage_max+1)
        if this_player_health - trap_damage < 0:
            contex = {'player_name': player_name, 'reason_name': location.name,
                      'text': f'Игрок {player_name} ловушка в {location.name} оказалась слишком коварна'}
            return render(request, 'Gameover.html', contex)
        Player.objects.filter(name=player_name).update(health=this_player_health - trap_damage)
        context = {'player_name': player_name, 'player_health': Player.objects.get(name=player_name).health,
                   'location_name': location.name, 'location_description': location.description,
                   'trap_exists': True, 'trap_found': False, 'trap_damage': trap_damage, 'location_map_id': location_map_id, }
    else:
        context = {'player_name': player_name, 'location_name': location.name,
                   'location_description': location.description,
                   'trap_exists': True, 'trap_found': True, 'trap_damage': 0, 'location_map_id': location_map_id, }
    return render(request, 'Location.html', context)

def Enter_dungeon_page(request):
    player_name = request.GET.get('player_name', 'Player')
    map_location = Map.objects.get(id=1)
    location = Location.objects.get(id=map_location.location_id)
    run_len = Map_len.objects.get(id=1).map_len
    current_len = int(len(Map.objects.all()))
    if current_len < run_len:
        for i in range(current_len+1, run_len+1):
            if randint(0, 11) < 6:
                Map.objects.create(id_number=i, location_id=randint(3, len(Location.objects.all())), enemy_class=0, is_it_enemy = False)
            else:
                Map.objects.create(id_number=i, enemy_class=randint(1, len(Location.objects.all())), is_it_enemy=True)
    for i in range(3, run_len+1):
        if randint(0, 11) < 5:
            Map.objects.filter(id_number=i).update(location_id=randint(3, len(Location.objects.all())), is_it_enemy = False)
        else:
            Map.objects.filter(id_number=i).update(location_id=0, enemy_class=randint(1, len(Enemy.objects.all())), is_it_enemy=True)
    context = {'player_name': player_name, 'location_name': location.name,
                   'location_description': location.description, 'location_map_id': 2}
    return render(request, 'Enter_dungeon.html', context)


def Winning_page(request):
    player_name = request.GET.get('player_name', 'Player')
    map_location = Map.objects.get(id_number=2)
    location = Location.objects.get(id_number=map_location.location_id)
    context = {'player_name': player_name, 'location_name': location.name,
               'location_description': location.description, 'location_map_id': 2}
    ##Player.objects.filter(name=player_name).update(health=10)
    Map_len.objects.all().update(map_len=7)
    return render(request, 'Winning_page.html', context)

def Gameover_page(request):
    player_name = request.GET.get('player_name', 'Player')
    reason_name = request.GET.get('reason_name', 'Время')
    text = f'{player_name}, хотел продолжить путь, но он слишком устал'
    context = {'player_name': player_name, 'reason_name': reason_name, 'text': text}
    ##Player.objects.filter(name=player_name).update(health=10)
    Map_len.objects.all().update(map_len=7)
    return render(request, 'Gameover.html', context)
