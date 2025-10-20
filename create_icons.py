#!/usr/bin/env python3
"""
Script para crear iconos PWA placeholder temporales
"""

import os

def create_svg_icon(size, output_path):
    """Crear un icono SVG y guardarlo como archivo"""
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{size}" height="{size}" xmlns="http://www.w3.org/2000/svg">
    <!-- Fondo degradado -->
    <defs>
        <linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" style="stop-color:#4f46e5;stop-opacity:1" />
            <stop offset="100%" style="stop-color:#7c3aed;stop-opacity:1" />
        </linearGradient>
    </defs>
    
    <!-- Fondo -->
    <rect width="{size}" height="{size}" fill="url(#grad1)" rx="20"/>
    
    <!-- Símbolo de dinero -->
    <text x="50%" y="50%" 
          font-family="Arial, sans-serif" 
          font-size="{size * 0.6}" 
          font-weight="bold"
          fill="white" 
          text-anchor="middle" 
          dominant-baseline="middle">$</text>
    
    <!-- Borde sutil -->
    <rect width="{size}" height="{size}" 
          fill="none" 
          stroke="rgba(255,255,255,0.2)" 
          stroke-width="2" 
          rx="20"/>
</svg>'''
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def main():
    print("🎨 Creando iconos PWA temporales...")
    
    # Crear directorio si no existe
    os.makedirs('static/icons', exist_ok=True)
    
    # Intentar crear con PIL/Pillow (preferido)
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        print("✅ Pillow detectado, creando iconos PNG de alta calidad...")
        
        for size in [192, 512]:
            # Crear imagen con degradado
            img = Image.new('RGB', (size, size), color=(79, 70, 229))
            draw = ImageDraw.Draw(img)
            
            # Agregar símbolo $
            try:
                # Intentar usar una fuente del sistema
                font_size = int(size * 0.5)
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Si no encuentra la fuente, usar la default
                font = ImageFont.load_default()
            
            # Dibujar el símbolo $
            text = "$"
            # Centrar el texto
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((size - text_width) // 2, (size - text_height) // 2 - int(size * 0.05))
            
            draw.text(position, text, fill=(255, 255, 255), font=font)
            
            # Guardar
            output_path = f'static/icons/icon-{size}x{size}.png'
            img.save(output_path, 'PNG')
            print(f"  ✅ Creado: {output_path}")
        
        print("\n✅ ¡Iconos PNG creados exitosamente!")
        
    except ImportError:
        # Si no tiene PIL, crear SVGs como alternativa
        print("⚠️  Pillow no está instalado")
        print("📝 Creando iconos SVG temporales...")
        
        for size in [192, 512]:
            output_path = f'static/icons/icon-{size}x{size}.svg'
            create_svg_icon(size, output_path)
            print(f"  ✅ Creado: {output_path}")
        
        print("\n⚠️  IMPORTANTE:")
        print("   Los iconos SVG son temporales.")
        print("   Para producción, instala Pillow y ejecuta de nuevo:")
        print("   pip install Pillow")
        print("   python create_icons.py")
    
    print("\n" + "="*60)
    print("📋 SIGUIENTE PASO:")
    print("="*60)
    print("\n✨ Los iconos temporales están listos para testing.")
    print("\n🎨 Para iconos profesionales:")
    print("   1. Ve a: https://www.pwabuilder.com/imageGenerator")
    print("   2. Sube tu logo/diseño")
    print("   3. Descarga los iconos")
    print("   4. Reemplaza los archivos en static/icons/")
    print("\n🚀 ¡Ahora puedes continuar con el despliegue!")

if __name__ == '__main__':
    main()
