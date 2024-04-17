from part_a import main as part_a_main
from part_b import main as part_b_main
from part_c import main as part_c_main
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if __name__ == "__main__":
    part_a_main()
    part_b_main()
    part_c_main()
