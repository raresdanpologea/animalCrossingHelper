from django.shortcuts import render
from .models import Item
from django.utils.timezone import localtime

def is_item_available_now(item):
    # If always available, return True immediately
    if item.always_available:
        return True
    now = localtime().time()
    start = item.start_time
    end = item.end_time

    if start <= end:
        # Same-day availability (e.g. 09:00–17:00)
        return start <= now <= end
    else:
        # Cross-midnight (e.g. 22:00–04:00)
        return now >= start or now <= end

def item_grid(request):
    # Get full set of items from DB, ordered by row and column
    items = Item.objects.all().order_by('row', 'column')

    # Build 5x16 grid with Items
    grid = [[None for _ in range(16)] for _ in range(5)]
    for item in items:
        grid[item.row][item.column] = item

    from datetime import datetime
    now = localtime()  # Use timezone-aware current time

    if request.method == 'POST':
        # IDs of items user claims to have (checked boxes)
        user_selected_ids = request.POST.getlist('selected_items')
        user_selected_ids = set(map(int, user_selected_ids))

        # All item IDs from DB
        all_item_ids = set(item.id for item in items)

        # Calculate missing IDs = all - selected
        missing_ids = all_item_ids - user_selected_ids
        missing_items = Item.objects.filter(id__in=missing_ids).order_by('row', 'column')

        available_now = [
            item for item in missing_items if is_item_available_now(item)
        ]

        return render(request, 'result.html', {
            'available_now': available_now,
            'current_time': now,
        })

    # GET request: render empty grid, user selects what they have
    return render(request, 'item_grid.html', {'grid': grid, 'current_time': now})
