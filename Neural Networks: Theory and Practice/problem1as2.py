import numpy as np
import torch
import timeit

# Define matrix multiplication using loops in Python
def matmul_python(A, B):
    C = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                C[i][j] += A[i][k] * B[k][j]
    return C

# Measure time for loop-based matrix multiplication
def time_matmul_python(shape):
    A = np.random.rand(*shape)
    B = np.random.rand(*shape)
    setup = f"from __main__ import matmul_python, A, B"
    return timeit.timeit("matmul_python(A, B)", setup=setup, number=1)

# Measure time for np.einsum
def time_matmul_einsum(shape):
    A = np.random.rand(*shape)
    B = np.random.rand(*shape)
    setup = f"import numpy as np; A = np.random.rand(*{shape}); B = np.random.rand(*{shape})"
    return timeit.timeit("np.einsum('ij,jk->ik', A, B)", setup=setup, number=1)

# Measure time for numpy on CPU
def time_matmul_numpy(shape):
    A = np.random.rand(*shape)
    B = np.random.rand(*shape)
    setup = f"import numpy as np; A = np.random.rand(*{shape}); B = np.random.rand(*{shape})"
    return timeit.timeit("np.dot(A, B)", setup=setup, number=1)

# Measure time for PyTorch on CPU
def time_matmul_pytorch_cpu(shape):
    A = torch.rand(*shape)
    B = torch.rand(*shape)
    setup = f"import torch; A = torch.rand({shape[0]}, {shape[1]}); B = torch.rand({shape[0]}, {shape[1]})"
    return timeit.timeit("torch.matmul(A, B)", setup=setup, number=1)

# Measure time for PyTorch on GPU
def time_matmul_pytorch_gpu(shape):
    if torch.cuda.is_available():
        A = torch.rand(*shape).cuda()
        B = torch.rand(*shape).cuda()
        setup = f"import torch; A = torch.rand({shape[0]}, {shape[1]}).cuda(); B = torch.rand({shape[0]}, {shape[1]}).cuda()"
        return timeit.timeit("torch.matmul(A, B)", setup=setup, number=1)
    else:
        return float('inf')  # Return infinity if GPU is not available
