clc;
clear;
close all;
faceDetector = vision.CascadeObjectDetector();

samples = dir('Samples dataset\*');

for m=3:6
   input_image = im2double((imread("./Samples dataset/" + samples(m).name +"/" + samples(m).name + ".png" )));
   smap_image = im2double((imread("./Samples dataset/" + samples(m).name +"/" + samples(m).name + "_SMap.png" )));
   dmap_image = im2double((imread("./Samples dataset/" + samples(m).name +"/" + samples(m).name + "_DMap.png" )));
 
    
    [path, name, ext] = fileparts(samples(m).name + ".png");
    path_folder='./FaceDetectMask/';


    seam_carving_look_ahead = 1; 

    faceLocation = step(faceDetector, input_image);
    
    resized_percent = 0.5;
    
    if ~isempty(faceLocation)
        % Extract the bounding box coordinates
        x = faceLocation(1, 1);
        y = faceLocation(1, 2);
        width = faceLocation(1, 3);
        height = faceLocation(1, 4);
        
        % Calculate the half width of the face bounding box
        %halfWidth = round(width / 2);
        halfWidthImage = size(input_image, 2) / 2;
        if width > halfWidthImage
            halfWidth = round(width / 50);
        else
            halfWidth = round(width / 3);
        end
        % Calculate the extended rectangle that starts from the bottom of the face
        % and extends half width to the left and right
        extendedY = min(y + height, size(input_image, 1)); % Bottom of the face
        extendedX = max(x - halfWidth, 1); % Ensure it doesn't go out of bounds on the left
        extendedWidth = min(x + width + halfWidth, size(input_image, 2)) - extendedX; % Ensure it doesn't go out of bounds on the right
        extendedRect = [extendedX, y, extendedWidth, size(input_image, 1) - extendedY];
        
        % Create a binary mask with the same size as the original image
        binaryMask = zeros(size(input_image, 1), size(input_image, 2));
        
        % Set the pixels within the extendedRect to 1
        binaryMask(y:y+height-1, x:x+width-1) = 1; % Face region
        binaryMask(extendedY:end, extendedX:extendedX+extendedWidth-1) = 1; % Extended body region
        
        % Display the binary mask
        figure; imshow(binaryMask,[]); title('Binary Mask for Face and Body');
        rgbMask = uint8(cat(3, binaryMask * 255, binaryMask * 255, binaryMask * 255));
        % Optional: Save the binary mask
        mask_path=path_folder+name+'_faceMask'+ext
        imwrite(rgbMask, mask_path);
        face_mask=im2double(imread(mask_path));
        energy_map = calculate_energy_map_face(input_image,face_mask, smap_image, dmap_image);
    else
        energy_map = calculate_energy_map(input_image, smap_image, dmap_image);
    end
    

    [final_image,energy_image] = perform_seam_carving(input_image, energy_map, resized_percent, seam_carving_look_ahead);
    
    figure,imshow(final_image, []);
    imwrite(final_image,"./Output/final_image_" + samples(m).name +".png" );


end








