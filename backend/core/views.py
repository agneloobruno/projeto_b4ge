from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from .models import Obra, InsumoAplicado
from .serializers import (
    ObraSerializer, InsumoAplicadoCreateSerializer, InsumoAplicadoSerializer
)
from .services.calculo import atualizar_totais_obra

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obra.objects.all().order_by("-id")
    serializer_class = ObraSerializer

    @action(detail=True, methods=["post"], url_path="itens")
    def adicionar_itens(self, request, pk=None):
        obra = self.get_object()
        itens = request.data if isinstance(request.data, list) else request.data.get("itens", [])
        if not isinstance(itens, list):
            return Response({"detail":"Esperado lista 'itens'."}, status=400)

        created = []
        for payload in itens:
            payload["obra"] = obra.id
            ser = InsumoAplicadoCreateSerializer(data=payload)
            ser.is_valid(raise_exception=True)
            item = ser.save()  # save() dispara cálculo no model
            created.append(item.id)

        atualizar_totais_obra(obra)
        out = InsumoAplicadoSerializer(InsumoAplicado.objects.filter(id__in=created), many=True)
        return Response({"criados": len(created), "itens": out.data}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], url_path="recalcular")
    def recalcular(self, request, pk=None):
        obra = self.get_object()
        # força recálculo de todos os itens
        for item in obra.itens_aplicados.select_related("insumo__material").all():
            item.save()
        atualizar_totais_obra(obra)
        return Response({"ok": True})


@api_view(["GET"])
def impactos_por_obra(request, obra_id: int):
    obra = get_object_or_404(Obra, id=obra_id)

    por_etapa = (
        InsumoAplicado.objects.filter(obra=obra)
        .values("etapa_obra")
        .annotate(
            energia_mj=Sum("energia_total_mj"),
            co2_kg=Sum("co2_total_kg"),
        ).order_by("etapa_obra")
    )

    etapas = [
        {
            "etapa_obra": r["etapa_obra"],
            "energia_gj": round((r["energia_mj"] or 0.0)/1000.0, 4),
            "co2_kg": round(r["co2_kg"] or 0.0, 2),
        }
        for r in por_etapa
    ]

    tot = InsumoAplicado.objects.filter(obra=obra).aggregate(
        energia_mj=Sum("energia_total_mj"),
        co2_kg=Sum("co2_total_kg"),
    )

    return Response({
        "obra_id": obra.id,
        "por_etapa": etapas,
        "energia_total_gj": round((tot["energia_mj"] or 0.0)/1000.0, 4),
        "co2_total_kg": round(tot["co2_kg"] or 0.0, 2),
    })
