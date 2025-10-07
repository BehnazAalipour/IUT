function [resized_image, resized_energy_map] = perform_seam_carving(original_image, energy_map, resize_ratio, look_ahead_steps)

    % resize_ratio between 0 to 1
    img_width = size(original_image, 2);
    resized_image = original_image;
    resized_energy_map = energy_map;
    num_seams = round(resize_ratio * img_width);
    
    for idx = 1 : num_seams
        [resized_image, resized_energy_map] = apply_seam_carving(resized_image, resized_energy_map, look_ahead_steps);
    end    
end