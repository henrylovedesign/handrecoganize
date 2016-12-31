#import skimage.data
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import selectivesearch
import cv2

def main():

    # loading astronaut image
    img = cv2.imread('/opt/henry/model_generator/MorpxData/classification/hands/ForTrain/negative/neck/neck36.jpg' )
     	
    # perform selective search
    img_lbl, regions = selectivesearch.selective_search(
        img, scale=500, sigma=0.05, min_size=10)
    print len(regions)
    candidates = set()
    for r in regions:
        # excluding same rectangle (with different segments)
        if r['rect'] in candidates:
            continue
        # excluding regions smaller than 2000 pixels
        if r['size'] < 1000:
            continue
        # distorted rects
        x, y, w, h = r['rect']
        if w / h > 2 or h / w > 2:
            continue
        candidates.add(r['rect'])

    # draw rectangles on the original image
    fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
    ax.imshow(img)
    for x, y, w, h in candidates:
        print x, y, w, h
        rect = mpatches.Rectangle(
            (x, y), w, h, fill=False, edgecolor='red', linewidth=1)
        ax.add_patch(rect)

    plt.show()

if __name__ == "__main__":
    main()
