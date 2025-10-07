function [updated_image, updated_energy_map] = apply_seam_carving(input_img, energy_img, look_ahead_steps)

img_height = size(input_img, 1);
img_width = size(input_img, 2);
cost_matrix = zeros(img_height, img_width);
cost_matrix(1, :) = energy_img(1, :);

for row = 2:img_height
    for col = 1:img_width
       if (col <= look_ahead_steps)
           cost_matrix(row, col) = energy_img(row, col) + min(cost_matrix(row-1, 1:col+look_ahead_steps));
       elseif (col >= img_width-look_ahead_steps)
           cost_matrix(row, col) = energy_img(row, col) + min(cost_matrix(row-1, col-look_ahead_steps:img_width));
       else
           cost_matrix(row, col) = energy_img(row, col) + min(cost_matrix(row-1, col-look_ahead_steps:col+look_ahead_steps));
       end
    end    
end

% find the column index of the minimum element in the last row of the cost matrix
min_seam_col = find(cost_matrix(end, :) == min(cost_matrix(end, :)), 1);
[updated_image, updated_energy_map] = delete_seam(cost_matrix, min_seam_col, energy_img, input_img, look_ahead_steps);

end