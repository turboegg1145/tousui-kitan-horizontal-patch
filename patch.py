# -*- coding: utf-8 -*-
"""
《灯穂奇譚》(Tousui Kitan) 简体中文汉化版 - 横版文字补丁生成器
Horizontal Text Patch Generator for Tousui Kitan (AOD Engine)

Author: turboegg1145
"""

import os
import sys

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

def apply_patch(input_path=None):
    # 1. 如果未传参数，优先检测当前目录；若不存在则支持交互式拖入/输入路径
    if not input_path:
        if len(sys.argv) > 1:
            input_path = sys.argv[1]
        elif os.path.exists("tosui_cn.exe"):
            input_path = "tosui_cn.exe"
        else:
            print("="*60)
            print("《灯穂奇譚》横版文字补丁生成器")
            print("="*60)
            input_path = input("请输入或直接将 tosui_cn.exe 拖入本窗口并回车: ").strip(' "\'')

    input_path = input_path.strip(' "\'')
    if not os.path.isfile(input_path):
        print(f"[错误] 指定的文件不存在: {input_path}")
        return False

    # 确定输出文件路径：默认保存在目标 exe 的同级目录下
    target_dir = os.path.dirname(os.path.abspath(input_path))
    output_path = os.path.join(target_dir, "tosui_cn_horizontal.exe")

    print(f"[*] 正在读取源文件: {input_path}")
    with open(input_path, 'rb') as f:
        data = bytearray(f.read())

    print(f"[*] 文件大小: {len(data)} 字节")
    
    # 逐项校验并打补丁
    for offset, orig_bytes, patch_bytes, desc in PATCHES:
        actual = bytes(data[offset:offset+len(orig_bytes)])
        if actual != orig_bytes:
            print(f"[错误] 偏移 0x{offset:X} 处的机器码不匹配!")
            print(f"  期望: {orig_bytes.hex()}, 实际: {actual.hex()} ({desc})")
            print("  请确认您提供的是否为未修改的标准《灯穂奇譚》汉化版 tosui_cn.exe。")
            return False
        
        data[offset:offset+len(patch_bytes)] = patch_bytes
        print(f"  [+] 应用修改 0x{offset:X}: {desc}")

    with open(output_path, 'wb') as f:
        f.write(data)

    print("\n" + "="*60)
    print(f"[成功] 横版补丁主程序已生成: {output_path}")
    print("="*60)
    print("使用说明: 直接双击运行生成的 tosui_cn_horizontal.exe 即可游玩横版！")
    return True

if __name__ == '__main__':
    apply_patch()
