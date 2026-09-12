# -*- coding: utf-8 -*-
"""
《灯穂奇譚》(Tousui Kitan) 简体中文汉化版 - 横版文字补丁生成器
Horizontal Text Patch Generator for Tousui Kitan (AOD Engine)

Author: turboegg1145
"""

import os
import sys
import hashlib
import shutil

# Patch table: (Offset, Original Bytes, Patched Bytes, Description)
PATCHES = [
    # 1. 坐标起始点：强制使用左上起始边距 (X0 = 40, Y0 = 30)
    (0x35909, b'\x75\x1A', b'\x90\x90', "Force horizontal start coordinates (Left/Top margins)"),

    # 2. 排版器模式参数：向排版子例程传递 mode=0 (Horizontal)
    (0x3688B, b'\x8B\x55\x08', b'\x31\xD2\x90', "Pass mode=0 (Horizontal) to typesetter"),

    # 3. 排版主循环：强制执行横向行推进逻辑
    (0x368F7, b'\x0F\x85\x8E\x01\x00\x00', b'\x90\x90\x90\x90\x90\x90', "Force horizontal line layout in typesetting loop"),

    # 4. 文本块格式化：强制选择横向排版路径
    (0x36F3A, b'\x0F\x85\xC4\x00\x00\x00', b'\x90\x90\x90\x90\x90\x90', "Force horizontal text block progression"),

    # 5. 字形包围盒：强制横向字符边界计算
    (0x37223, b'\x75\x18', b'\x90\x90', "Force horizontal glyph bounding calculation"),

    # 6. 字符渲染回调：传递 mode=0
    (0x372E6, b'\x8B\x45\x08', b'\x31\xC0\x90', "Pass mode=0 to glyph renderer"),

    # 7. 字符步进宽度：X 轴累加单字宽度
    (0x37339, b'\x75\x0B', b'\x90\x90', "Advance X by character width"),

    # 8. 块提交逻辑：横向段落提交
    (0x37375, b'\x75\x69', b'\x90\x90', "Force horizontal block commit"),

    # 9. 辅助排版分支 1
    (0x3755B, b'\x75\x65', b'\x90\x90', "Layout branch 0x437556 horizontal bypass"),

    # 10. 辅助排版分支 2
    (0x37746, b'\x75\x65', b'\x90\x90', "Layout branch 0x437741 horizontal bypass"),

    # 11. 禁用标点分类转换，始终使用标准正向变换矩阵 (0x9f4e78)
    (0x380D0, b'\x75\x1E', b'\xEB\x1E', "Bypass vertical punctuation rotation matrix"),

    # 12. 第二次 GetGlyphOutlineA 强制使用无旋转矩阵
    (0x38140, b'\x75\x25', b'\xEB\x25', "Force unrotated MAT2 for glyph rasterization"),

    # 13. 彻底旁路标点符号右上角偏移与竖排位移
    (0x38272, b'\x0F\x85\x15\x01\x00\x00', b'\xE9\x16\x01\x00\x00\x90', "Bypass vertical punctuation coordinate shift"),
]

def apply_patch(input_exe="tosui_cn.exe", output_exe="tosui_cn_horizontal.exe"):
    if not os.path.exists(input_exe):
        print(f"[错误] 未在当前目录下找到原始可执行文件: {input_exe}")
        print("请将本脚本放置于《灯穂奇譚》游戏根目录（包含 tosui_cn.exe 的文件夹）运行。")
        return False

    print(f"[*] 正在读取: {input_exe}")
    with open(input_exe, 'rb') as f:
        data = bytearray(f.read())

    print(f"[*] 文件大小: {len(data)} 字节")
    
    # 验证与应用补丁
    for offset, orig_bytes, patch_bytes, desc in PATCHES:
        actual = bytes(data[offset:offset+len(orig_bytes)])
        if actual != orig_bytes:
            print(f"[警告/错误] 偏移 0x{offset:X} 处的字节不匹配!")
            print(f"  期望: {orig_bytes.hex()}, 实际: {actual.hex()} ({desc})")
            print("  请确认您的 tosui_cn.exe 是否为标准的汉化版 v1.0。")
            return False
        
        data[offset:offset+len(patch_bytes)] = patch_bytes
        print(f"  [+] 成功应用补丁 0x{offset:X}: {desc}")

    with open(output_exe, 'wb') as f:
        f.write(data)

    print("\n" + "="*60)
    print(f"[完成] 横版主程序生成成功: {output_exe}")
    print("="*60)
    print("使用说明: 直接双击运行生成的 tosui_cn_horizontal.exe 即可体验横版阅读！")
    return True

if __name__ == '__main__':
    in_file = sys.argv[1] if len(sys.argv) > 1 else "tosui_cn.exe"
    out_file = sys.argv[2] if len(sys.argv) > 2 else "tosui_cn_horizontal.exe"
    apply_patch(in_file, out_file)
