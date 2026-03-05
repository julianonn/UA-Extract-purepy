import timeit
import statistics
from typing import Dict, List
from ua_extract import DeviceDetector


# Realistic web traffic UAs only (browsers + mobile apps)
WEB_TRAFFIC_UAS = [
    # Desktop browsers - Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    
    # Desktop browsers - Firefox
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0',
    
    # Desktop browsers - Safari
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    
    # Desktop browsers - Edge
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
    
    # Mobile browsers - Safari iOS
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1',
    
    # Mobile browsers - Chrome Android
    'Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    
    # Mobile browsers - Firefox Android
    'Mozilla/5.0 (Android; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
    'Mozilla/5.0 (Android 14; Mobile; rv:121.0) Gecko/121.0 Firefox/121.0',
    
    # Mobile app - Facebook app
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBAV/428.0.0.37.28;...]',
    'Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.58 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/428.0.0.37.28;...]',
    
    # Mobile app - Instagram app
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 280.0.0.39.111',
    'Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/99.0.4844.58 Mobile Safari/537.36 Instagram 280.0.0.39.111',
    
    # Mobile app - Generic webview
    'Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36 (com.myapp)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 myapp/1.0',
    
    # Masked UAs (privacy-reduced)
    # Safari with minimal info
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)',
    # Chrome with Android system UA only
    'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
]

# Create variants for a larger dataset
EXPANDED_UAS = WEB_TRAFFIC_UAS + [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.7 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/120.0.0.0',
]


def measure_cold_parse(uas: List[str], iterations: int = 3) -> Dict[str, float]:
    """Measure parse time with fresh detector (no cache)."""
    def parse_batch():
        for ua in uas:
            dd = DeviceDetector(ua)
            dd.parse()
    
    # Run multiple times and collect total times in milliseconds
    times_ms = []
    for _ in range(iterations):
        elapsed = timeit.timeit(parse_batch, number=1) * 1000  # Convert to ms
        times_ms.append(elapsed)
    
    return {
        'min': min(times_ms),
        'max': max(times_ms),
        'avg': statistics.mean(times_ms),
        'stdev': statistics.stdev(times_ms) if len(times_ms) > 1 else 0,
    }


def measure_warm_parse(uas: List[str], iterations: int = 5) -> Dict[str, float]:
    """Measure parse time with warm cache (repeated parses)."""
    # Warm up cache first
    for ua in uas:
        dd = DeviceDetector(ua)
        dd.parse()
    
    # Now measure warm cache performance
    def parse_batch_warm():
        for ua in uas:
            dd = DeviceDetector(ua)
            dd.parse()
    
    # Run multiple times and collect times in milliseconds
    times_ms = []
    for _ in range(iterations):
        elapsed = timeit.timeit(parse_batch_warm, number=1) * 1000  # Convert to ms
        times_ms.append(elapsed)
    
    return {
        'min': min(times_ms),
        'max': max(times_ms),
        'avg': statistics.mean(times_ms),
        'stdev': statistics.stdev(times_ms) if len(times_ms) > 1 else 0,
    }


def measure_per_ua_time(uas: List[str], repeats_per_ua: int = 10) -> Dict[str, float]:
    """Measure parse time per individual UA (repeated multiple times for precision)."""
    times = {}
    
    for ua in uas:
        def parse_single():
            dd = DeviceDetector(ua)
            dd.parse()
        
        # Run each UA multiple times to get measurable timings
        elapsed_ms = timeit.timeit(parse_single, number=repeats_per_ua) * 1000
        
        # Extract category for grouping
        if 'iPhone' in ua or 'iPad' in ua:
            category = 'iOS'
        elif 'Android' in ua:
            category = 'Android'
        elif 'Facebook' in ua or 'FBAN' in ua:
            category = 'FB App'
        elif 'Instagram' in ua:
            category = 'IG App'
        elif 'Windows' in ua:
            category = 'Windows'
        elif 'Macintosh' in ua:
            category = 'macOS'
        elif 'X11; Linux' in ua:
            category = 'Linux'
        else:
            category = 'Other'
        
        if category not in times:
            times[category] = []
        # Divide by repeats to get per-UA average
        times[category].append(elapsed_ms / repeats_per_ua)
    
    # Summarize by category
    summary = {}
    for category, values in times.items():
        summary[category] = {
            'count': len(values),
            'avg_ms': statistics.mean(values),
            'min_ms': min(values),
            'max_ms': max(values),
        }
    
    return summary


def print_report():
    """Run full performance suite and print results."""
    print('\n' + '='*70)
    print('UA-EXTRACT-PUREPY PERFORMANCE BENCHMARK')
    print('(Web traffic only: browsers + mobile apps)')
    print('='*70)
    
    print(f'\nDataset size: {len(WEB_TRAFFIC_UAS)} common UAs, {len(EXPANDED_UAS)} expanded')
    
    # Cold cache test
    print('\n' + '-'*70)
    print('COLD PARSE (fresh detector, no cache)')
    print('-'*70)
    cold_small = measure_cold_parse(WEB_TRAFFIC_UAS, iterations=5)
    cold_large = measure_cold_parse(EXPANDED_UAS, iterations=5)
    
    print(f'Small dataset ({len(WEB_TRAFFIC_UAS)} UAs):')
    print(f'  Total time: {cold_small["avg"]:.2f}ms (avg)')
    print(f'  Per UA:     {(cold_small["avg"]/len(WEB_TRAFFIC_UAS)):.2f}ms')
    print(f'  Range:      {cold_small["min"]:.2f}ms - {cold_small["max"]:.2f}ms')
    
    print(f'\nLarge dataset ({len(EXPANDED_UAS)} UAs):')
    print(f'  Total time: {cold_large["avg"]:.2f}ms (avg)')
    print(f'  Per UA:     {(cold_large["avg"]/len(EXPANDED_UAS)):.2f}ms')
    print(f'  Range:      {cold_large["min"]:.2f}ms - {cold_large["max"]:.2f}ms')
    
    # Warm cache test
    print('\n' + '-'*70)
    print('WARM PARSE (cache populated, repeated parses)')
    print('-'*70)
    warm_small = measure_warm_parse(WEB_TRAFFIC_UAS, iterations=5)
    warm_large = measure_warm_parse(EXPANDED_UAS, iterations=5)
    
    print(f'Small dataset ({len(WEB_TRAFFIC_UAS)} UAs):')
    print(f'  Total time: {warm_small["avg"]:.2f}ms (avg)')
    print(f'  Per UA:     {(warm_small["avg"]/len(WEB_TRAFFIC_UAS)):.2f}ms')
    print(f'  Range:      {warm_small["min"]:.2f}ms - {warm_small["max"]:.2f}ms')
    
    print(f'\nLarge dataset ({len(EXPANDED_UAS)} UAs):')
    print(f'  Total time: {warm_large["avg"]:.2f}ms (avg)')
    print(f'  Per UA:     {(warm_large["avg"]/len(EXPANDED_UAS)):.2f}ms')
    print(f'  Range:      {warm_large["min"]:.2f}ms - {warm_large["max"]:.2f}ms')
    
    # Cache impact
    print('\n' + '-'*70)
    print('CACHE IMPACT (warm vs cold)')
    print('-'*70)
    speedup_small = cold_small['avg'] / warm_small['avg']
    speedup_large = cold_large['avg'] / warm_large['avg']
    print(f'Small dataset: {speedup_small:.1f}x faster (warm cache)')
    print(f'Large dataset: {speedup_large:.1f}x faster (warm cache)')
    
    # Per-category breakdown
    print('\n' + '-'*70)
    print('BREAKDOWN BY PLATFORM (single parse, cold cache)')
    print('-'*70)
    breakdown = measure_per_ua_time(WEB_TRAFFIC_UAS)
    for category in sorted(breakdown.keys()):
        stats = breakdown[category]
        print(f'{category:12} | {stats["count"]:2d} UAs | '
              f'avg: {stats["avg_ms"]:.3f}ms | '
              f'min: {stats["min_ms"]:.3f}ms | '
              f'max: {stats["max_ms"]:.3f}ms')
    
    print('\n' + '='*70 + '\n')


if __name__ == '__main__':
    print_report()
