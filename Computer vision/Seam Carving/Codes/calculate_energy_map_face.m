function energy_map = calculate_energy_map_face(img, img_1, saliency_map, depth_map)
    
    img_height = size(img, 1);
    img_width = size(img, 2);
    energy_map = zeros(img_height, img_width);

    img_1=img_1(:,:,1);

    gray_img = rgb2gray(img);
    [grad_image, gradient_direction] = imgradient(gray_img);

    % Use Sobel filter to find edges
    edge_image = edge(gray_img, "sobel");
    % Resize edge and gradient maps to match the size of the grayscale image
    edge_image = imresize(edge_image, size(gray_img));


    thresholds = multithresh(depth_map, 4);
    segmented = imquantize(depth_map, thresholds);


    % Combine different energy components into the total energy map
    energy_map = (0.5 *segmented) + (0.05 * saliency_map) + (0.05 * grad_image) + (0.1 * im2double(edge_image)+(0.3*img_1));

    % Display the gradient and total energy maps
    figure, imshow(grad_image, []);
    figure, imshow(energy_map, []);
    
end
