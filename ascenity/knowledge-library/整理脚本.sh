#!/bin/bash
# Ascenity 07 Knowledge Library 一键整理脚本
# 在 Mac「终端机」贴上执行即可。安全、可重复执行（已搬过的会跳过）。
# 只搬「最上层散книги」，不动你四个既有资料夹里面的东西。

set -u
LIB="$HOME/Library/Mobile Documents/com~apple~CloudDocs/ASCENITY/07 Knowledge Library"

if [ ! -d "$LIB" ]; then
  echo "找不到资料夹：$LIB"
  echo "如果 iCloud 还没下载，先在 Finder 打开该资料夹让它同步，再重跑。"
  exit 1
fi

cd "$LIB" || exit 1
shopt -s nullglob 2>/dev/null

# 建立目标资料夹（既有的不受影响，缺的才建）
mkdir -p "企业管理" "Marketing & Strategy" "Personal Growth" "Fitness" "财富与投资"

# 搬移函式：move_to <目标资料夹> <关键字1> [关键字2 ...]
move_to () {
  dest="$1"; shift
  for kw in "$@"; do
    for f in *"$kw"*; do
      # 别把目标资料夹自己搬进去
      [ "$f" = "$dest" ] && continue
      if [ -e "$f" ]; then
        mv -v "$f" "$dest/" 2>/dev/null && echo "  → 移入 [$dest]：$f"
      fi
    done
  done
}

echo "开始整理…"
echo ""

echo "[企业管理]"
move_to "企业管理" "一人公司" "第一性原理"

echo "[Marketing & Strategy]"
move_to "Marketing & Strategy" "個人品牌獲利" "个人品牌获利"

echo "[Personal Growth]"
move_to "Personal Growth" "大人學破局思考" "大人学破局思考" "非暴力沟通" "生命数字密码"

echo "[财富与投资]"
move_to "财富与投资" "納瓦爾寶典" "纳瓦尔宝典" "投资最重要的事" "思考致富" "致富心态" "穷查理宝典" "穷爸爸富爸爸" "薛兆丰经济学"

echo ""
echo "======== 整理完成，各资料夹现况 ========"
for d in "企业管理" "Marketing & Strategy" "Personal Growth" "财富与投资" "Fitness"; do
  echo ""
  echo "📁 $d"
  ls -1 "$d" 2>/dev/null | sed 's/^/   /'
done

echo ""
echo "还留在最上层（应该只剩这四个资料夹本身，若有漏网之鱼请告诉我）："
ls -1p | grep '/$'
