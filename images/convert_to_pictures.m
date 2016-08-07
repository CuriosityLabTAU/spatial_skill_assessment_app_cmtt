% convert_to_pictures
clear all; close all;
for i=60%2:2:64
   filename = sprintf('CMTT_A_Order1_Page_%02d.jpg', i);
   x = imread(filename);
   imshow(x)
   D = x(1:(end/2), (end/20):(end/2), :);
   C = x(1:(end/2), (end/2+1):(end*9/10), :);
   B = x((end/2+1):end, (end/20):(end/2), :);
   A = x((end/2+1):end, (end/2+1):(end*9/10), :);
   
   figure;imshow(A)
   figure;imshow(B)
   figure;imshow(C)
   figure;imshow(D)
   
   imwrite(A, sprintf('%s_A.jpg', filename(1:(end-4))));
   imwrite(B, sprintf('%s_B.jpg', filename(1:(end-4))));
   imwrite(C, sprintf('%s_C.jpg', filename(1:(end-4))));
   imwrite(D, sprintf('%s_D.jpg', filename(1:(end-4))));
end