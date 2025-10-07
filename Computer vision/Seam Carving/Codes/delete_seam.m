function [updated_image, updated_energy_map] = delete_seam(cost_matrix, seam_index, energy_matrix, input_image, look_ahead_steps)

    img_height = size(input_image, 1);
    img_width = size(input_image, 2);
    
    updated_energy_map = zeros(img_height, img_width-1);
    updated_image = zeros(img_height, img_width-1, 3);
    
    for row = img_height : -1 : 1
        input_image(row, seam_index, :) = [1, 0, 0];
        energy_matrix(row, seam_index) = 0;
        
        updated_energy_map(row, :) = energy_matrix(row, [1:seam_index-1, seam_index+1:img_width]);
        updated_image(row, :, :) = input_image(row, [1:seam_index-1, seam_index+1:img_width], :);
        
        if row ~= 1
            search_range = max([seam_index - look_ahead_steps, 1]) : min([seam_index + look_ahead_steps, img_width]);
            next_pixel = find(cost_matrix(row-1, search_range) == min(cost_matrix(row-1, search_range)), 1);
            seam_index = max([seam_index - look_ahead_steps, 1]) - 1 + next_pixel; % find next cell in seam  
        end        
    end
    
    imshow(input_image, []);
end