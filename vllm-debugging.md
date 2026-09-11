# vLLM Local Inference --- Debugging & Working Configuration

## 1. Environment

  Component                  Previous / Initial         Current / Working
  -------------------------- -------------------------- -------------------------------------
  OS                         Ubuntu 26.04 LTS on WSL2   Ubuntu 26.04 LTS on WSL2
  Python                     3.12.14                    **3.12.14**
  GPU                        RTX 5060 Ti 16 GB          **RTX 5060 Ti 16 GB (SM 12.0)**
  PyTorch                    2.13.0+cu130               **2.13.0+cu130**
  vLLM                       0.28.0                     **0.28.0**
  FlashInfer                 0.6.16.post3               **0.6.16.post3**
  CUDA reported by PyTorch   13.0                       **13.0**
  nvcc                       13.0.88                    **13.0.88**
  CUDA NVCC package          13.3.73                    **13.0.88**
  CUDA CRT                   13.3.73                    **13.0.88**
  CUDA CCCL                  13.3.x                     **13.0.85**
  CUDA NVVM                  13.3.73                    **13.0.88**
  CUDA Runtime               13.3.29                    **13.0.96**
  CUDA Toolkit package       13.0.3.0                   **13.0.3.0**
  GCC/G++                    Missing                    **Installed via `build-essential`**

Model: - `Qwen/Qwen2.5-1.5B-Instruct`

Validation: - `torch.cuda.is_available()` → `True` - `pip check` →
`No broken requirements found` - vLLM API server → **Started
successfully**

------------------------------------------------------------------------

## 2. Debugging Changes

### 2.1 vLLM V2 / WSL2 UVA issue

**Error**

``` text
RuntimeError: UVA is not available
```

**Change**

``` bash
export VLLM_USE_V2_MODEL_RUNNER=0
```

**Reason:** vLLM V2 encountered a CUDA UVA compatibility issue in the
WSL2 + Blackwell environment.

### 2.2 CUDA compiler path

**Error**

``` text
PermissionError: [Errno 13] Permission denied: 'nvcc'
```

**Change**

``` bash
export PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/bin:$PATH"
```

**Reason:** the venv contained `nvcc`, but its directory was not
correctly available through `PATH`.

### 2.3 Missing Linux compiler toolchain

**Error**

``` text
RuntimeError: Failed to find C compiler
```

**Change**

``` bash
sudo apt update
sudo apt install -y build-essential
```

**Reason:** TorchInductor/compiled CUDA components require GCC/G++ and
related build tools.

### 2.4 Mixed CUDA 13.0 / 13.3 components

**Error**

``` text
CUDA compiler and CUDA toolkit headers are incompatible
```

**Change:** aligned the CUDA compiler/toolkit components to the CUDA
13.0 stack:

``` text
nvidia-cuda-nvcc    13.3.73  -> 13.0.88
nvidia-cuda-cccl    13.3.x   -> 13.0.85
nvidia-nvvm         13.3.73  -> 13.0.88
nvidia-cuda-runtime 13.3.29  -> 13.0.96
nvidia-cuda-crt     13.3.73  -> 13.0.88
```

**Validation:** CUDA header changed from `CUDART_VERSION 13030` to
`13000`.

### 2.5 FlashInfer linker could not find CUDA runtime

**Error**

``` text
cannot find -lcudart
```

**Cause:** FlashInfer searched `cu13/lib64`, while `libcudart.so.13`
existed under `cu13/lib`.

**Changes**

``` bash
export LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib:/usr/lib/wsl/lib:$LIBRARY_PATH"
export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib:/usr/lib/wsl/lib:$LD_LIBRARY_PATH"

mkdir -p "$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib64"

ln -sf ../lib/libcudart.so.13 \
"$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib64/libcudart.so"
```

### 2.6 FlashInfer cache reset

After changing CUDA compiler/runtime components:

``` bash
rm -rf "$HOME/.cache/flashinfer/0.6.16.post3/120f/cached_ops/sampling"
```

This forces the affected FlashInfer sampling component to rebuild
against the corrected CUDA environment.

------------------------------------------------------------------------

## 3. Final Startup Environment

``` bash
export VLLM_USE_V2_MODEL_RUNNER=0

export PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/bin:$PATH"

export LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib:/usr/lib/wsl/lib:$LIBRARY_PATH"

export LD_LIBRARY_PATH="$VIRTUAL_ENV/lib/python3.12/site-packages/nvidia/cu13/lib:/usr/lib/wsl/lib:$LD_LIBRARY_PATH"

vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

Server status:

``` text
Application startup complete.
```

`GET /` returning `404` is expected because `/` is not a defined vLLM
API endpoint.

------------------------------------------------------------------------

## 4. Key Concepts

-   **WSL2:** Linux environment running on Windows; CUDA behavior
    differs from native Linux in some areas.
-   **CUDA Driver:** Provides GPU driver functionality; WSL exposes the
    Windows NVIDIA driver to Linux.
-   **CUDA Toolkit:** Development stack containing `nvcc`, headers,
    NVVM, CRT and CUDA libraries.
-   **nvcc:** NVIDIA CUDA compiler used to compile `.cu` code.
-   **TorchInductor:** PyTorch compiler that generates/compiles
    optimized kernels.
-   **FlashInfer:** Optimized GPU kernels used by LLM inference
    workloads, including sampling.
-   **GCC/G++:** Linux C/C++ compilers required by generated/native
    extensions.
-   **Linker (`ld`):** Combines compiled objects with libraries to
    create shared libraries such as `sampling.so`.
-   **`PATH`:** Locates executable programs such as `nvcc`.
-   **`LIBRARY_PATH`:** Helps the compiler/linker locate libraries
    during builds.
-   **`LD_LIBRARY_PATH`:** Helps the runtime loader locate shared
    libraries.
-   **UVA:** CUDA Unified Virtual Addressing; the vLLM V2 issue required
    disabling the V2 runner in this WSL2 setup.
-   **CUDA version alignment:** Compiler, headers, runtime, CRT, NVVM
    and related components must be compatible to avoid compile/link
    failures.
-   **Compute capability 12.0:** Blackwell architecture target of the
    RTX 5060 Ti; FlashInfer compiled kernels for the GPU architecture.

------------------------------------------------------------------------

## 5. Debugging Flow

``` text
vLLM startup
   ↓
UVA error
   ↓
Disable V2 model runner
   ↓
nvcc path error
   ↓
Add CUDA bin to PATH
   ↓
C compiler missing
   ↓
Install build-essential
   ↓
CUDA 13.0 / 13.3 mismatch
   ↓
Align CUDA components to 13.0
   ↓
FlashInfer linker: -lcudart missing
   ↓
Fix lib64 runtime path/symlink
   ↓
Clear FlashInfer cache
   ↓
vLLM server starts successfully
```

## 6. Current Status

**Working:** GPU → CUDA → PyTorch → TorchInductor → FlashInfer → vLLM →
Qwen2.5-1.5B-Instruct → OpenAI-compatible API server.

Next verification:

``` bash
curl http://localhost:8000/v1/models
```

Then test inference through:

``` text
POST /v1/chat/completions
```
