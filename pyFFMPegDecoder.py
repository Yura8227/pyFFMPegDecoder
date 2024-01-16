"""
Simple ffmpeg-python pipe out example
"""
import ffmpeg
import numpy as np
import os
import imshow as imshow


class ffmpeg_wrapper():
    def __init__(self) -> None:
        pass

    def init(self, input_file, output_file):
        # Set input file
        self.input_file = input_file
        
        probe = ffmpeg.probe(self.input_file)
        
        # This shows only the 1st video stream. You may need to change this
        video_info = next(s for s in probe['streams'] if s['codec_type'] == 'video')
        
        video_width = int(video_info['width'])
        video_height = int(video_info['height'])
        num_frames = int(video_info['nb_frames'])

        # Set output file - for raw video 
        self.output_file = output_file

        if output_file is None:
            self.output_file = 'pipe:'

        if os.path.exists(self.output_file):
            os.remove(self.output_file)

        process = (
            ffmpeg
            .input(self.input_file)
            .output(self.output_file, format='rawvideo', pix_fmt='rgb24')
            #.run_async(pipe_stdout=True, pipe_stderr=True)
            .run(pipe_stdout=True, pipe_stderr=True)
        )

        num_got = 0

        while True or num_got < num_frames:
            frame = process.stdout.read(video_width*video_height*3)
            if not frame:
                continue
            # Do something with frame
            raw_frame = (
                np
                .frombuffer(frame, np.uint8)
                .reshape([-1,video_height,video_width,3])                
            )

            imshow.imshow(raw_frame)
            num_got += 1

        process.stdout.close()
 

if __name__ == "__main__":

    input_file = "input.mp4"
    output_file = None #"output.mp4"
    
    decoder = ffmpeg_wrapper()
    decoder.init(input_file, output_file)

    decoder.run()



