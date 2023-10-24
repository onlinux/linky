def temperature_to_rgb(temperature):
    # Define the temperature range and corresponding RGB colors
    temperature_range = [(0, (0, 0, 255)),   # 0°C: Blue
                         (30, (255, 165, 0)),  # 30°C: Orange
                         (40, (255, 0, 0))]   # 40°C: Red
    
    # Handle cases where the temperature is below 0°C or above 40°C
    if temperature <= 0:
        return (0, 0, 255)  # Blue
    elif temperature >= 40:
        return (255, 0, 0)  # Red
    
    # Iterate through the temperature range
    for i in range(len(temperature_range) - 1):
        low_temp, low_color = temperature_range[i]
        high_temp, high_color = temperature_range[i + 1]
        
        # Check if the temperature falls within this range
        if low_temp <= temperature < high_temp:
            # Linear interpolation between the two colors based on temperature
            t = (temperature - low_temp) / (high_temp - low_temp)
            r = int(low_color[0] + t * (high_color[0] - low_color[0]))
            g = int(low_color[1] + t * (high_color[1] - low_color[1]))
            b = int(low_color[2] + t * (high_color[2] - low_color[2]))
            
            return (r, g, b)
    
    return (0, 0, 0)  # Default: Black

# Test the function with a temperature value
# temperature = 25  # Change this to the temperature you want to convert
# rgb_color = temperature_to_rgb(temperature)
# print(f"Temperature: {temperature}°C -> RGB Color: {rgb_color}")
