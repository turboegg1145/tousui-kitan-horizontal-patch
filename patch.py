# -*- coding: utf-8 -*-
"""
《灯穂奇譚》(Tousui Kitan) 简体中文汉化版 - 横版排版补丁源码
Horizontal Text Layout Patch for Tousui Kitan (AOD Engine)

Author: turboegg1145
"""

import sys
import os

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

def apply_patch(input_path, output_path):
    if not os.path.isfile(input_path):
        print(f"Error: input file not found: {input_path}")
        return False

    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    for offset, orig_bytes, patch_bytes, desc in PATCHES:
        actual = bytes(data[offset:offset+len(orig_bytes)])
        if actual != orig_bytes:
            print(f"Error: byte mismatch at offset 0x{offset:X} ({desc})")
            return False
        data[offset:offset+len(patch_bytes)] = patch_bytes

    with open(output_path, 'wb') as f:
        f.write(data)

    print(f"Successfully generated: {output_path}")
    return True

if __name__ == '__main__':
    src = sys.argv[1] if len(sys.argv) > 1 else "tosui_cn.exe"
    dst = sys.argv[2] if len(sys.argv) > 2 else "tosui_cn_horizontal.exe"
    apply_patch(src, dst)
