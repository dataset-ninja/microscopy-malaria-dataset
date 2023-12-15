The authors of the **Microscopy Malaria Dataset** explore the application of point-of-care diagnostics in microscopy and computer vision for practical issues, especially in low-income, high disease burden areas. The experts annotated thick blood smears, *plasmodium* instances were annotated. For sputum samples, the experts annotated tuberculosis bacilli (*tb bacillus*). Additionally, in images of stool samples, annotations encompassed the eggs of *hookworm*, *taenia*, and *hymenolepsis nana*.

## Motivation

Conventional light microscopy remains the standard for diagnosing conditions like malaria, particularly in low-resource settings. While newer technologies exist, the simplicity and versatility of microscopy make it suitable for resource-constrained areas. However, the shortage of skilled technicians hinders its effectiveness, leading to diagnoses based solely on clinical signs and symptoms.

To address the challenges, the authors emphasize the development of point-of-care diagnostics using common resources like microscopes and smartphones. Leveraging the widespread ownership of smartphones in developing regions, the authors propose a setup with significant potential for remote and automated diagnosis. Computer vision methods play a crucial role in automating microscopical assessments within the limitations of camera optics and image analysis accuracy.

## Disease-Specific Considerations

**Malaria.** The gold standard for malaria diagnosis is the microscopical examination of stained blood smear samples. Thick blood smears, being more sensitive, are recommended for screening plasmodium parasites. The study explores the use of deep learning for accurate malaria detection, addressing challenges like low parasitemia.

**Tuberculosis** diagnosis relies on the demonstration of mycobacteria in clinical specimens. The Ziehl-Neelsen stain is commonly used, and the study evaluates the application of deep learning for TB detection in sputum samples. Challenges in rural, developing-world settings are considered due to the expense and time-consuming nature of current diagnostic methods.

**Intestinal Parasites.** Identifying helminth eggs involves microscopy of fecal samples. The study explores the potential of deep learning in distinguishing helminth eggs from fecal impurities, addressing challenges in accurate diagnosis.

## Data Acquisition

The authors present the experimental setup utilized for data collection and system prototype testing. To deploy computer vision methods for decision support and automated diagnostics, they recognized the need for a suitable deployment platform. Existing digital microscopes and imaging solutions were either costly or limited to specific microscope models, rendering them unsuitable for the task. Additionally, the authors observed challenges with existing low-cost smartphone adapters, particularly their sensitivity to movement, which could lead to alignment issues.

<img src="https://github.com/dataset-ninja/microscopy-malaria-dataset/assets/78355358/be63f894-b6d7-40cb-95d7-fd5dc9b63902" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Microscope smartphone adapter: design of components (left), 3D-printed adapter mounted on microscope (center), smartphone inserted into adapter (right).</span>

<img src="https://github.com/dataset-ninja/microscopy-malaria-dataset/assets/78355358/a3fff6f2-941b-4ac6-bcd1-4656f6cd264d" alt="image" width="800">

<span style="font-size: smaller; font-style: italic;">Image of thick blood smear with Giemsa stain, taken with the apparatus shown above. Detail on right shows several P. falciparum clearly visible.</span>

The attachment mechanism seamlessly couples with the microscope eyepiece (ocular). The adjustment mechanism is strategically designed to allow users to correctly align a smartphone of almost any model with the focal point of the eyepiece. Achieved through sliders and side-holders, this mechanism facilitates precise positioning of the phone. The locking mechanism ensures the smartphone remains in position once the correct alignment is achieved. Users can easily slide the smartphone in and out of the adapter without compromising the pre-set alignment, enhancing usability.

## Imaging and Annotation

Using the described setup, the authors captured malaria images from thick blood smears stained with Field stain at x1000 magnification. Tuberculosis (TB) images were obtained from fresh sputum, stained with ZN (Ziehl Neelsen) stain, and examined under x1000 magnification. For intestinal parasites, images were captured from slides of a wet preparation, involving a portion of stool sample mixed in a drop of normal saline, and examined under x400 magnification.

In the annotation phase, laboratory experts provided input on the object locations within the images. This information was systematically recorded using annotation software tailored for the task. The experts meticulously identified bounding boxes around each object of interest in every image. For thick blood smear images, plasmodium were annotated, resulting in 7245 objects across 1182 images. In sputum samples, tuberculosis bacilli were annotated, totaling 9969 objects in 1218 images. In stool samples, the eggs of hookworm, Taenia, and Hymenolepsis nana were annotated, comprising 162 objects in 1217 images. This annotated dataset serves as a valuable resource for further research in the domain of microscopy and automated diagnostics.
