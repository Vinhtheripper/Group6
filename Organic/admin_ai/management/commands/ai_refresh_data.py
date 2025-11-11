from django.core.management.base import BaseCommand
from admin_ai.core_ai.exporter import export_all
from admin_ai.core_ai.retrain_loop import rebuild_from_csv
import chromadb
from django.conf import settings

class Command(BaseCommand):
    help = "Tự động export dữ liệu từ ORM, retrain embedding và in thống kê."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("🚀 Bắt đầu làm mới dữ liệu AI Greenest..."))
        
        try:
            export_all()
            self.stdout.write(self.style.SUCCESS("✅ Đã export toàn bộ dữ liệu ORM ra CSV."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Lỗi export: {e}"))
            return

        try:
            rebuild_from_csv()
            self.stdout.write(self.style.SUCCESS("✅ Đã rebuild embeddings từ CSV."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Lỗi rebuild: {e}"))
            return

        # Kiểm tra số vector hiện tại
        client = chromadb.PersistentClient(path=f"{settings.BASE_DIR}/chroma_db")
        col = client.get_or_create_collection("greenest_daily")
        count = col.count()

        self.stdout.write(self.style.SUCCESS(f" ChromaDB hiện chứa {count} vector embeddings."))
        self.stdout.write(self.style.HTTP_INFO(" Hoàn tất cập nhật dữ liệu AI Greenest!"))
