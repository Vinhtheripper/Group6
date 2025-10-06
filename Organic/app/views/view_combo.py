from app.models import Combo
from django.shortcuts import render, get_object_or_404



def combodetail(request, combo_id):
    combo = get_object_or_404(Combo, id=combo_id)
    combo_items = combo.comboitem_set.select_related("product")
    related_combos = Combo.objects.exclude(id=combo.id)[:4]  

    return render(request, "app/combodetail.html", {
        "combo": combo,
        "combo_items": combo_items,
        "related_combos": related_combos,
    })