
import multiprocessing

from init2_p1 import get_res
def run_p1():
    num_processes = 2

    # 创建进程池
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 并行调用get_res函数10次
        results = pool.map(get_res, range(num_processes))

    # 合并结果
    combined_results = []
    for result in results:
        combined_results.extend(result)

    print(f"Combined results length: {len(combined_results)}")
    return combined_results

# if __name__ == "__main__":
combined_results = run_p1()

