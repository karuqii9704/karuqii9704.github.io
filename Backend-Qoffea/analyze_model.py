"""
Script untuk menganalisis model AI best.pt
Menampilkan informasi tentang arsitektur model, input/output, dan parameter
"""

import torch
import json
from pathlib import Path

def analyze_yolo_model(model_path):
    """Analisis model YOLO/PyTorch"""
    print("=" * 80)
    print("ANALISIS MODEL AI - QOFFEA COFFEE GRADING")
    print("=" * 80)
    
    try:
        # Load model
        print(f"\n📁 Loading model dari: {model_path}")
        model = torch.load(model_path, map_location='cpu')
        
        print("\n✅ Model berhasil dimuat!")
        
        # Cek tipe model
        print(f"\n📊 Tipe Data Model: {type(model)}")
        
        # Jika model adalah dictionary (format YOLO/Ultralytics)
        if isinstance(model, dict):
            print("\n🔍 STRUKTUR MODEL (Dictionary Keys):")
            for key in model.keys():
                print(f"  - {key}")
            
            # Informasi epoch dan training
            if 'epoch' in model:
                print(f"\n📈 Training Epoch: {model['epoch']}")
            
            # Informasi model
            if 'model' in model:
                print("\n🧠 ARSITEKTUR MODEL:")
                model_obj = model['model']
                print(f"  - Type: {type(model_obj)}")
                
                if hasattr(model_obj, 'names'):
                    print(f"\n🏷️  KELAS DETEKSI (Classes):")
                    names = model_obj.names
                    if isinstance(names, dict):
                        for idx, name in names.items():
                            print(f"    {idx}: {name}")
                    elif isinstance(names, list):
                        for idx, name in enumerate(names):
                            print(f"    {idx}: {name}")
                
                if hasattr(model_obj, 'yaml'):
                    print(f"\n⚙️  KONFIGURASI MODEL:")
                    yaml_config = model_obj.yaml
                    if isinstance(yaml_config, dict):
                        for key, value in yaml_config.items():
                            if key not in ['backbone', 'head']:  # Skip kompleks
                                print(f"    {key}: {value}")
            
            # Informasi optimizer
            if 'optimizer' in model:
                print("\n🎯 OPTIMIZER INFO:")
                opt = model['optimizer']
                if opt and hasattr(opt, 'param_groups'):
                    print(f"  - Learning Rate: {opt.param_groups[0]['lr']}")
            
            # Training args
            if 'train_args' in model:
                print("\n📋 TRAINING ARGUMENTS:")
                args = model['train_args']
                if isinstance(args, dict):
                    important_args = ['imgsz', 'batch', 'epochs', 'data']
                    for key in important_args:
                        if key in args:
                            print(f"  - {key}: {args[key]}")
            
            # Metrics
            if 'best_fitness' in model:
                print(f"\n🎖️  Best Fitness Score: {model['best_fitness']}")
            
        else:
            # Jika model langsung
            print("\n🧠 MODEL OBJECT:")
            if hasattr(model, 'names'):
                print(f"\n🏷️  Classes: {model.names}")
        
        # Hitung total parameters
        print("\n💾 INFORMASI PARAMETER:")
        if isinstance(model, dict) and 'model' in model:
            model_obj = model['model']
            if hasattr(model_obj, 'parameters'):
                total_params = sum(p.numel() for p in model_obj.parameters())
                trainable_params = sum(p.numel() for p in model_obj.parameters() if p.requires_grad)
                print(f"  - Total Parameters: {total_params:,}")
                print(f"  - Trainable Parameters: {trainable_params:,}")
                print(f"  - Model Size: ~{total_params * 4 / (1024*1024):.2f} MB")
        
        print("\n" + "=" * 80)
        print("KESIMPULAN ANALISIS")
        print("=" * 80)
        
        print("\n📝 Ringkasan:")
        print("  Model ini kemungkinan adalah model YOLO (You Only Look Once)")
        print("  untuk deteksi dan klasifikasi biji kopi berdasarkan grade/kualitas.")
        print("\n  Model dapat:")
        print("  ✓ Mendeteksi biji kopi dalam gambar")
        print("  ✓ Mengklasifikasikan ke dalam beberapa grade (A, B, C)")
        print("  ✓ Memberikan confidence score untuk setiap deteksi")
        
        print("\n💡 Rekomendasi untuk Backend:")
        print("  1. Gunakan framework: Flask/FastAPI")
        print("  2. Library: ultralytics, torch, opencv-python, pillow")
        print("  3. Input: Upload gambar (JPG/PNG)")
        print("  4. Output: JSON dengan grade, persentase, dan koordinat deteksi")
        print("  5. Endpoint API: /predict, /analyze, /health")
        
        return model
        
    except Exception as e:
        print(f"\n❌ Error saat menganalisis model: {str(e)}")
        print(f"   Tipe error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    model_path = Path(__file__).parent / "models" / "best.pt"
    
    if not model_path.exists():
        print(f"❌ Model tidak ditemukan di: {model_path}")
        print("   Pastikan file best.pt ada di folder models/")
    else:
        analyze_yolo_model(model_path)
