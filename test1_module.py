class test1:
    def __init__(self, imgs, sigma=1, kernel_size=5, weak_pixel=75, strong_pixel=255, lowthreshold=0.05, highthreshold=0.15):
        self.imgs = imgs
        self.sigma = sigma
        self.kernel_size = kernel_size
        self.weak_pixel = weak_pixel
        self.strong_pixel = strong_pixel
        self.lowthreshold = lowthreshold
        self.highthreshold = highthreshold
        # Initialize other variables if necessary

    def detect(self):
        # Your detect function logic
        pass
