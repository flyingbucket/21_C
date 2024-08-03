import multiprocessing

from init2_p2 import GA_init_partial

# 定义主函数
num_processes = 20  # 定义进程数
def run_p2(i,j,current_space):
    '''多线程调用get_res函数，返回多线程调用的合并结果'''
    # 创建进程池
    with multiprocessing.Pool(processes=num_processes) as pool:
        # 并行调用GA_init_partial函数20次
        results = pool.starmap(GA_init_partial, [(i,j,current_space) for _ in range(num_processes)])

    # 合并结果
    combined_results = []
    for result in results:
        combined_results.extend(result)

    print(f"Combined results length: {len(combined_results)}")
    return combined_results

if __name__ == "__main__":
    multiprocessing.freeze_support()

