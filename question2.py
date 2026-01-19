"""
Strategic Tile Shatter Game - Bottom-Up Dynamic Programming Solution
Procedural Approach with Detailed Step-by-Step Comments

This solution finds the maximum points obtainable by shattering tiles optimally.
When tile k is shattered, points earned = multipliers[left] * multipliers[k] * multipliers[right]
"""


def max_shatter_points(tile_multipliers):
    """
    Calculate maximum points from shattering tiles using dynamic programming.
    
    The algorithm works by finding the optimal order to shatter tiles.
    Key insight: When we shatter tile k last in a range, its neighbors
    are the boundaries of that range at shatter time.
    
    Args:
        tile_multipliers (list): Multiplier values for each tile
    
    Returns:
        int: Maximum total points achievable
    """
    
    # Handle edge cases
    if not tile_multipliers:
        return 0
    
    if len(tile_multipliers) == 1:
        return 0
    
    # Pre-processing: Add 1 at start and end to handle boundaries
    # This simplifies the logic by treating boundaries as multipliers of 1
    tiles = [1] + tile_multipliers + [1]
    n = len(tiles)
    
    # Initialize DP table
    # dp[i][j] = maximum points from shattering all tiles between index i and j (exclusive)
    # We exclude tiles[i] and tiles[j] from the range to be shattered
    dp = [[0] * n for _ in range(n)]
    
    # Fill the DP table from smaller ranges to larger ranges
    # range_length represents how many tiles apart the indices are
    for range_length in range(2, n):
        # Iterate over all possible left boundaries
        for left_idx in range(n - range_length):
            # Calculate the right boundary based on range length
            right_idx = left_idx + range_length
            
            # Try all possible tiles to shatter last in this range
            # The last tile shattered will have multipliers[left_idx] and multipliers[right_idx] as neighbors
            for last_tile in range(left_idx + 1, right_idx):
                # Calculate points from shattering tile at last_tile position
                # This tile gets: left_boundary * this_tile * right_boundary
                points_from_last = tiles[left_idx] * tiles[last_tile] * tiles[right_idx]
                
                # Total points = points from left subrange + points from right subrange + points from shattering last tile
                total_points = dp[left_idx][last_tile] + dp[last_tile][right_idx] + points_from_last
                
                # Update DP table if this gives better result
                dp[left_idx][right_idx] = max(dp[left_idx][right_idx], total_points)
    
    # The answer is the maximum points from the entire range
    # tiles[0] and tiles[n-1] are the boundaries (both are 1), rest are original tiles
    return dp[0][n - 1]

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("STRATEGIC TILE SHATTER - PROCEDURAL DYNAMIC PROGRAMMING")
    print("=" * 70)
    
    # Test Case 1: Multiple tiles
    print("\nTest Case 1: Multiple Tiles")
    print("-" * 70)
    
    test_tiles_1 = [3, 1, 5, 8]
    result_1 = max_shatter_points(test_tiles_1)
    expected_1 = 167
    
    print(f"Tile Multipliers: {test_tiles_1}")
    print(f"Calculated Points: {result_1}")
    print(f"Expected Points:   {expected_1}")
    
    status_1 = "PASS" if result_1 == expected_1 else "FAIL"
    print(f"Test Status: {status_1}")
    
    # Test Case 2: Two tiles
    print("\nTest Case 2: Two Tiles")
    print("-" * 70)
    
    test_tiles_2 = [1, 5]
    result_2 = max_shatter_points(test_tiles_2)
    expected_2 = 10
    
    print(f"Tile Multipliers: {test_tiles_2}")
    print(f"Calculated Points: {result_2}")
    print(f"Expected Points:   {expected_2}")
    
    status_2 = "PASS" if result_2 == expected_2 else "FAIL"
    print(f"Test Status: {status_2}")
    
    print("\n" + "=" * 70)
    if status_1 == "PASS" and status_2 == "PASS":
        print("ALL TESTS PASSED!")
    print("=" * 70 + "\n")


