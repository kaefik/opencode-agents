#!/usr/bin/env python3
"""
Extract projects and tasks from Singularity backup JSON file.
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional


def load_backup(file_path: str) -> Dict[str, Any]:
    """Load Singularity backup JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def build_maps(data: Dict[str, Any]) -> tuple:
    """Build mapping dictionaries for related entities."""
    project_map = {p['id']: p for p in data['data'].get('projects', [])}
    task_map = {t['id']: t for t in data['data'].get('tasks', [])}
    taskgroup_map = {tg['id']: tg for tg in data['data'].get('taskGroups', [])}
    note_map = {n['id']: n for n in data['data'].get('notes', [])}
    tag_map = {t['id']: t for t in data['data'].get('tags', [])}
    
    return project_map, task_map, taskgroup_map, note_map, tag_map


def format_date(date_str: Optional[str]) -> str:
    """Format ISO date string to readable format."""
    if not date_str or date_str == 'N/A':
        return 'N/A'
    try:
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M')
    except:
        return date_str


def extract_note_content(note: Optional[Dict[str, Any]]) -> str:
    """Extract text content from Quill Delta note."""
    if not note:
        return ''
    content = note.get('content', '')
    if isinstance(content, str):
        try:
            delta_ops = json.loads(content)
            text = ''.join(op.get('insert', '') for op in delta_ops if isinstance(op, dict))
            return text.strip()
        except:
            return content.strip()
    elif isinstance(content, list):
        text = ''.join(op.get('insert', '') for op in content if isinstance(op, dict))
        return text.strip()
    return ''


def extract_projects(projects: List[Dict[str, Any]], project_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and format projects with related info."""
    extracted = []
    
    for p in projects:
        if p.get('_removed', 0) != 0:
            continue
            
        project = {
            'id': p['id'],
            'title': p.get('title', ''),
            'start': format_date(p.get('start', '')) if p.get('start') else '',
            'end': format_date(p.get('end', '')) if p.get('end') else '',
            'color': p.get('color', ''),
            'emoji': p.get('emoji', ''),
            'parent': p.get('parent', ''),
            'parent_title': '',
            'isNotebook': p.get('isNotebook', False),
        }
        
        # Get parent title
        if project['parent'] and project['parent'] in project_map:
            project['parent_title'] = project_map[project['parent']].get('title', '')
        
        extracted.append(project)
    
    return extracted


def extract_tasks(tasks: List[Dict[str, Any]], 
                  project_map: Dict[str, Any],
                  task_map: Dict[str, Any],
                  taskgroup_map: Dict[str, Any],
                  note_map: Dict[str, Any],
                  tag_map: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract and format tasks with all related info."""
    extracted = []
    
    for t in tasks:
        if t.get('_removed', 0) != 0:
            continue
        
        # Project info
        project_id = t.get('projectId')
        project = project_map.get(project_id) if project_id else None
        
        # Task group info
        group_id = t.get('group')
        group = taskgroup_map.get(group_id) if group_id else None
        
        # Parent task info
        parent_id = t.get('parent')
        parent = task_map.get(parent_id) if parent_id else None
        
        # Note info
        note_id = t.get('note')
        note = note_map.get(note_id) if note_id else None
        
        # Tags info
        tag_ids = t.get('tags', [])
        tags = [tag_map.get(tid, {}).get('title', '') for tid in tag_ids if tid in tag_map]
        
        # Recurrence info
        recurrence = t.get('recurrence')
        recurrence_info = {}
        if recurrence:
            repeat_type = recurrence.get('repeat', {}).get('type', '')
            recurrence_info = {
                'type': repeat_type,
                'next_time': format_date(recurrence.get('nextTime', '')),
                'paused': recurrence.get('paused', False),
            }
        
        task = {
            'id': t['id'],
            'title': t.get('title', ''),
            'project_id': project_id or '',
            'project_title': project.get('title', '') if project else '',
            'group_id': group_id or '',
            'group_title': group.get('title', '') if group else '',
            'parent_id': parent_id or '',
            'parent_title': parent.get('title', '') if parent else '',
            'parent_order': t.get('parentOrder', ''),
            'start': format_date(t.get('start', '')) if t.get('start') else '',
            'deadline': format_date(t.get('deadline', '')) if t.get('deadline') else '',
            'created_date': format_date(t.get('createdDate', '')) if t.get('createdDate') else '',
            'journal_date': format_date(t.get('journalDate', '')) if t.get('journalDate') else '',
            'time_length': t.get('timeLength', ''),
            'priority': t.get('priority', ''),
            'priority_text': {0: 'Низкий', 1: 'Высокий', 2: 'Срочный'}.get(t.get('priority'), ''),
            'complete': t.get('complete', 0),
            'state': t.get('state', ''),
            'checked': t.get('checked', False),
            'deferred': t.get('deferred', False),
            'use_time': t.get('useTime', False),
            'note': extract_note_content(note) if note else '',
            'tags': tags,
            'notifies': t.get('notifies', []),
            'alarm_notify': t.get('alarmNotify', False),
            'recurrence': recurrence_info,
            'schedule_order': t.get('scheduleOrder', ''),
            'seen_today': t.get('seenToday', ''),
            'is_note': t.get('isNote', False),
            'show_in_basket': t.get('showInBasket', False),
            'delete_date': t.get('deleteDate', ''),
        }
        
        extracted.append(task)
    
    return extracted


def print_projects_table(projects: List[Dict[str, Any]]):
    """Print projects as a markdown table."""
    print("## Проекты\n")
    print("| ID | Название | Родитель | Эмодзи | Цвет |")
    print("|----|----------|----------|--------|------|")
    
    for p in sorted(projects, key=lambda x: x['title']):
        parent = f"({p['parent_title']})" if p['parent_title'] else ''
        print(f"| {p['id']} | {p['title']} {parent} | {p['parent'] or ''} | {p['emoji'] or ''} | {p['color'] or ''} |")
    
    print(f"\n**Всего проектов**: {len(projects)}\n")


def print_tasks_summary(tasks: List[Dict[str, Any]]):
    """Print tasks summary statistics."""
    total = len(tasks)
    with_project = len([t for t in tasks if t['project_title']])
    with_deadline = len([t for t in tasks if t['deadline']])
    with_recurrence = len([t for t in tasks if t['recurrence']])
    with_notes = len([t for t in tasks if t['note']])
    with_parent = len([t for t in tasks if t['parent_title']])
    with_notifies = len([t for t in tasks if t['notifies']])
    with_tags = len([t for t in tasks if t['tags']])
    
    print("## Статистика задач\n")
    print(f"- **Всего задач**: {total}")
    print(f"- **С проектом**: {with_project}")
    print(f"- **С дедлайном**: {with_deadline}")
    print(f"- **Повторяющиеся**: {with_recurrence}")
    print(f"- **С заметками**: {with_notes}")
    print(f"- **Подзадачи**: {with_parent}")
    print(f"- **С напоминаниями**: {with_notifies}")
    print(f"- **С тегами**: {with_tags}\n")


def filter_tasks_by_status(tasks: List[Dict[str, Any]], status_filter: str, include_basket: bool = True) -> List[Dict[str, Any]]:
    """Filter tasks by completion status and basket status.
    
    In Singularity:
    - Task completion: 'checked' field
      * checked=1: task is completed
      * checked=0: task is not completed
    
    - Task deletion: 'showInBasket' field
      * showInBasket=True: task is in basket (deleted)
      * showInBasket=False or missing: task is active
    
    - The 'complete' field is used for parent tasks with subtasks to show percentage.
    
    Args:
        tasks: List of tasks
        status_filter: 'all', 'complete' (checked=1), 'incomplete' (checked=0)
        include_basket: If False, exclude tasks in basket (showInBasket=True)
    
    Returns:
        Filtered list of tasks
    """
    # Filter by completion status
    if status_filter == 'complete':
        filtered = [t for t in tasks if t.get('checked', 0) == 1]
    elif status_filter == 'incomplete':
        filtered = [t for t in tasks if t.get('checked', 0) == 0]
    else:
        filtered = list(tasks)
    
    # Filter by basket status
    if not include_basket:
        filtered = [t for t in filtered if not t.get('show_in_basket', False)]
    
    return filtered


def print_tasks_by_project(tasks: List[Dict[str, Any]]):
    """Print tasks grouped by project."""
    print("## Задачи по проектам\n")
    
    # Group tasks by project
    project_tasks: Dict[str, List[Dict[str, Any]]] = {}
    for t in tasks:
        project_name = t['project_title'] or 'Без проекта'
        if project_name not in project_tasks:
            project_tasks[project_name] = []
        project_tasks[project_name].append(t)
    
    # Sort by project name
    for project_name in sorted(project_tasks.keys()):
        print(f"### {project_name}\n")
        print("| ID | Название | Дедлайн | Приоритет | Статус |")
        print("|----|----------|---------|-----------|--------|")
        
        for t in sorted(project_tasks[project_name], key=lambda x: x['created_date']):
            priority = t['priority_text'] or ''
            status = f"{t['complete']}%" if t['complete'] else ''
            print(f"| {t['id']} | {t['title'][:50]}{'...' if len(t['title']) > 50 else ''} | {t['deadline']} | {priority} | {status} |")
        
        print(f"\n**Всего**: {len(project_tasks[project_name])}\n")


def save_to_json(data: Dict[str, Any], output_file: str, status_filter: str = 'all'):
    """Save extracted data to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        data['filter'] = {'status': status_filter}
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"\nДанные сохранены в: {output_file}")


def save_to_markdown(projects: List[Dict[str, Any]], tasks: List[Dict[str, Any]], output_file: str, 
                      status_filter: str = 'all', basket_mode: str = 'include'):
    """Save extracted data to Markdown file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Singularity Projects and Tasks Export\n\n")
        f.write(f"**Дата экспорта**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        # Filter status info
        filter_info = {
            'all': 'Все задачи',
            'complete': 'Только выполненные (checked=1)',
            'incomplete': 'Только не выполненные (checked=0)'
        }
        
        # Basket mode info
        basket_info = {
            'include': 'Включая задачи из корзины',
            'exclude': 'Исключая задачи из корзины',
            'only': 'Только задачи из корзины (удаленные)'
        }
        
        f.write(f"**Фильтр статуса**: {filter_info.get(status_filter, 'Все задачи')}\n")
        f.write(f"**Корзина**: {basket_info.get(basket_mode, 'Включая задачи из корзины')}\n\n")
        
        # Projects
        f.write("## Проекты\n\n")
        f.write("| ID | Название | Родитель | Эмодзи | Цвет |\n")
        f.write("|----|----------|----------|--------|------|\n")
        for p in sorted(projects, key=lambda x: x['title']):
            parent = f"({p['parent_title']})" if p['parent_title'] else ''
            f.write(f"| {p['id']} | {p['title']} {parent} | {p['parent'] or ''} | {p['emoji'] or ''} | {p['color'] or ''} |\n")
        f.write(f"\n**Всего проектов**: {len(projects)}\n\n")
        
        # Tasks summary
        total = len(tasks)
        with_project = len([t for t in tasks if t['project_title']])
        with_deadline = len([t for t in tasks if t['deadline']])
        with_recurrence = len([t for t in tasks if t['recurrence']])
        with_notes = len([t for t in tasks if t['note']])
        with_parent = len([t for t in tasks if t['parent_title']])
        
        f.write("## Статистика задач\n\n")
        f.write(f"- **Всего задач**: {total}\n")
        f.write(f"- **С проектом**: {with_project}\n")
        f.write(f"- **С дедлайном**: {with_deadline}\n")
        f.write(f"- **Повторяющиеся**: {with_recurrence}\n")
        f.write(f"- **С заметками**: {with_notes}\n")
        f.write(f"- **Подзадачи**: {with_parent}\n\n")
        
        # Tasks by project
        f.write("## Задачи по проектам\n\n")
        project_tasks: Dict[str, List[Dict[str, Any]]] = {}
        for t in tasks:
            project_name = t['project_title'] or 'Без проекта'
            if project_name not in project_tasks:
                project_tasks[project_name] = []
            project_tasks[project_name].append(t)
        
        for project_name in sorted(project_tasks.keys()):
            f.write(f"### {project_name}\n\n")
            f.write("| ID | Название | Дедлайн | Приоритет | Статус | Родитель | Группа |")
            f.write("\n|----|----------|---------|-----------|--------|----------|--------|\n")
            for t in sorted(project_tasks[project_name], key=lambda x: x['created_date']):
                priority = t['priority_text'] or ''
                status = f"{t['complete']}%" if t['complete'] else ''
                parent = t['parent_title'][:30] + '...' if len(t['parent_title']) > 30 else t['parent_title']
                group = t['group_title'][:20] + '...' if len(t['group_title']) > 20 else t['group_title']
                title = t['title'][:60] + '...' if len(t['title']) > 60 else t['title']
                f.write(f"| {t['id']} | {title} | {t['deadline']} | {priority} | {status} | {parent} | {group} |\n")
            f.write(f"\n**Всего**: {len(project_tasks[project_name])}\n\n")
        
        # Tasks with notes
        tasks_with_notes = [t for t in tasks if t['note']]
        if tasks_with_notes:
            f.write("## Задачи с заметками\n\n")
            for t in tasks_with_notes[:50]:
                f.write(f"### {t['title']}\n")
                f.write(f"- **ID**: {t['id']}\n")
                f.write(f"- **Проект**: {t['project_title'] or 'N/A'}\n")
                f.write(f"- **Заметка**: {t['note'][:500]}{'...' if len(t['note']) > 500 else ''}\n\n")
        
        # Tasks with deadlines
        tasks_with_deadline = [t for t in tasks if t['deadline']]
        if tasks_with_deadline:
            f.write("## Задачи с дедлайнами\n\n")
            f.write("| ID | Название | Проект | Дедлайн | Приоритет |\n")
            f.write("|----|----------|---------|---------|-----------|\n")
            for t in sorted(tasks_with_deadline, key=lambda x: x['deadline']):
                title = t['title'][:50] + '...' if len(t['title']) > 50 else t['title']
                f.write(f"| {t['id']} | {title} | {t['project_title'] or 'N/A'} | {t['deadline']} | {t['priority_text']} |\n")
            f.write("\n")
        
        # Recurring tasks
        tasks_with_recurrence = [t for t in tasks if t['recurrence']]
        if tasks_with_recurrence:
            f.write("## Повторяющиеся задачи\n\n")
            f.write("| ID | Название | Проект | Тип | Следующее | Пауза |\n")
            f.write("|----|----------|---------|-----|-----------|-------|\n")
            for t in sorted(tasks_with_recurrence, key=lambda x: x['title']):
                title = t['title'][:50] + '...' if len(t['title']) > 50 else t['title']
                r = t['recurrence']
                f.write(f"| {t['id']} | {title} | {t['project_title'] or 'N/A'} | {r.get('type', '')} | {r.get('next_time', '')} | {'Да' if r.get('paused') else 'Нет'} |\n")
            f.write("\n")
        
        # Tasks with notifies
        tasks_with_notifies = [t for t in tasks if t['notifies']]
        if tasks_with_notifies:
            f.write("## Задачи с напоминаниями\n\n")
            f.write("| ID | Название | Проект | Напоминания (мин) | Будильник |\n")
            f.write("|----|----------|---------|-------------------|-----------|\n")
            for t in tasks_with_notifies:
                title = t['title'][:50] + '...' if len(t['title']) > 50 else t['title']
                f.write(f"| {t['id']} | {title} | {t['project_title'] or 'N/A'} | {t['notifies']} | {'Да' if t['alarm_notify'] else 'Нет'} |\n")
            f.write("\n")
    
    print(f"Данные сохранены в: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description='Extract projects and tasks from Singularity backup JSON file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Примеры использования:
  python3 extract_singularity_data.py                           # Все задачи
  python3 extract_singularity_data.py --status complete        # Только выполненные
  python3 extract_singularity_data.py --status incomplete      # Только не выполненные
  python3 extract_singularity_data.py /path/to/backup.json      # Указать файл
  python3 extract_singularity_data.py --status incomplete backup.json
        '''
    )
    parser.add_argument(
        'backup_file',
        nargs='?',
        default='data/singularity_backup_2026-02-11.json',
        help='Путь к файлу бэкапа Singularity (по умолчанию: data/singularity_backup_2026-02-11.json)'
    )
    parser.add_argument(
        '--status',
        choices=['all', 'complete', 'incomplete'],
        default='all',
        help='Фильтр по статусу выполнения: all (все), complete (выполненные, checked=1), incomplete (не выполненные, checked=0)'
    )
    parser.add_argument(
        '--include-basket',
        action='store_true',
        default=True,
        help='Включать задачи из корзины (по умолчанию: включены). Используйте --no-include-basket для исключения.'
    )
    parser.add_argument(
        '--no-include-basket',
        action='store_false',
        dest='include_basket',
        help='Исключить задачи из корзины'
    )
    parser.add_argument(
        '--basket-only',
        action='store_true',
        default=False,
        help='Только задачи из корзины (удаленные)'
    )
    parser.add_argument(
        '--json-output',
        default='extracted_data.json',
        help='Путь к выходному JSON файлу'
    )
    parser.add_argument(
        '--md-output',
        default='extracted_data.md',
        help='Путь к выходному Markdown файлу'
    )
    
    args = parser.parse_args()
    
    print(f"Загрузка файла: {args.backup_file}")
    data = load_backup(args.backup_file)
    
    print("Построение маппингов...")
    project_map, task_map, taskgroup_map, note_map, tag_map = build_maps(data)
    
    print("Извлечение проектов...")
    projects = extract_projects(data['data'].get('projects', []), project_map)
    
    print("Извлечение задач...")
    all_tasks = extract_tasks(data['data'].get('tasks', []), project_map, task_map, taskgroup_map, note_map, tag_map)
    
    print(f"Фильтрация задач (статус: {args.status}, корзина: {'включена' if args.include_basket else 'исключена'})...")
    
    # Filter by basket status if --basket-only is specified
    if args.basket_only:
        tasks = [t for t in all_tasks if t.get('show_in_basket', False)]
        # Then filter by completion status
        if args.status == 'complete':
            tasks = [t for t in tasks if t.get('checked', 0) == 1]
        elif args.status == 'incomplete':
            tasks = [t for t in tasks if t.get('checked', 0) == 0]
    else:
        tasks = filter_tasks_by_status(all_tasks, args.status, args.include_basket)
    
    print(f"\n✓ Проектов: {len(projects)}")
    print(f"✓ Задач (всего): {len(all_tasks)}")
    print(f"✓ Задач (после фильтрации): {len(tasks)}")
    
    # Determine basket mode
    if args.basket_only:
        basket_mode = 'only'
    elif not args.include_basket:
        basket_mode = 'exclude'
    else:
        basket_mode = 'include'
    
    # Save to JSON
    save_to_json({
        'projects': projects,
        'tasks': tasks,
        'export_date': datetime.now().isoformat(),
        'total_tasks': len(all_tasks),
        'basket_mode': basket_mode
    }, args.json_output, args.status)
    
    # Save to Markdown
    save_to_markdown(projects, tasks, args.md_output, args.status, basket_mode)
    
    # Print to console
    filter_names = {
        'all': 'Все задачи',
        'complete': 'Выполненные (checked=1)',
        'incomplete': 'Не выполненные (checked=0)'
    }
    
    basket_info = ''
    if args.basket_only:
        basket_info = ' [ТОЛЬКО КОРЗИНА]'
    elif not args.include_basket:
        basket_info = ' [БЕЗ КОРЗИНЫ]'
    
    print("\n" + "="*80)
    print(f"Фильтр: {filter_names.get(args.status, args.status)}{basket_info}\n")
    print_projects_table(projects)
    print_tasks_summary(tasks)
    print("="*80)


if __name__ == '__main__':
    main()
