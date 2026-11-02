from __future__ import annotations

def _self_peak_ws_mb(*, facade: facade.Any) -> facade.Optional[float]:
    if facade.platform.system() != 'Windows':
        return None
    import ctypes
    import ctypes.wintypes as wt

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [('cb', wt.DWORD), ('PageFaultCount', wt.DWORD), ('PeakWorkingSetSize', ctypes.c_size_t), ('WorkingSetSize', ctypes.c_size_t), ('QuotaPeakPagedPoolUsage', ctypes.c_size_t), ('QuotaPagedPoolUsage', ctypes.c_size_t), ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t), ('QuotaNonPagedPoolUsage', ctypes.c_size_t), ('PagefileUsage', ctypes.c_size_t), ('PeakPagefileUsage', ctypes.c_size_t)]
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    psapi = ctypes.WinDLL('psapi', use_last_error=True)
    kernel32.GetCurrentProcess.restype = wt.HANDLE
    psapi.GetProcessMemoryInfo.restype = wt.BOOL
    psapi.GetProcessMemoryInfo.argtypes = [wt.HANDLE, ctypes.POINTER(PROCESS_MEMORY_COUNTERS), wt.DWORD]
    h = kernel32.GetCurrentProcess()
    c = PROCESS_MEMORY_COUNTERS()
    c.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    ok = psapi.GetProcessMemoryInfo(h, ctypes.byref(c), c.cb)
    return c.PeakWorkingSetSize / 1024 / 1024 if ok else None
