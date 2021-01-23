# Seeded Tunes - seeded_tunes

This is a project to take a single seed number and generate:

* A fictional "music scene" with...
  * a pool of people attached
  * multiple fictional "record labels" each with...
    * a pool of people taken from the scene pool
    * multiple fictional "artists" attached each with ...
      * people drawn from the label pool
      * one or more incarnations of the group, each with...
        * multiple fictional "albums" released each with...
          * generated artwork for multiple formats (CD, 12in etc) generated in SVG and [ImageMagick](http://www.imagemagick.org)
          * multiple tracks of generated music
  * a Family Tree of all the artists and their incarnations and personnel, in the style created by [Pete Frame](https://familyofrock.net/)

**_With a single seed, a whole music scene and discography is created!_**

```mermaid
erDiagram
    SCENE ||--|{ LABEL : contains
    SCENE ||--|{ SCENEPOOL : involves
    SCENEPOOL ||--|{ PERSON : contains
    LABELPOOL ||--|{ PERSON : contains
    ARTISTPOOL ||--|{ PERSON : contains
    INCARNATIONPOOL ||--|{ PERSON : contains
    LABEL ||--|{ ARTIST : contains
    LABEL ||--|| LABELPOOL : uses
    ARTIST ||--|{ INCARNATION : "exists with"
    ARTIST ||--|| ARTISTPOOL : uses
    INCARNATION ||--|{ ALBUM : releases
    INCARNATION ||--|| INCARNATIONPOOL : uses
    ALBUM ||--|{ TRACK : contains
    ALBUM ||--|| ALBUMARTWORK : has
    ALBUMARTWORK {
        string bgColour
    }
    PERSON {
        string firstName
        string surname
    }
    SCENE {
        int seed
        int yearStart
        int yearEnd
    }
    LABEL {
        string name
        int yearStart
        int yearEnd
    }
    ARTIST {
        string name
        text biography
        int yearStart
        int yearEnd
    }
    INCARNATION {
        int yearStart
        int yearEnd
    }
    ALBUM {
        string name
        int year
    }
    TRACK {
        string name
        int length
        file music
    }

```

| Entity      |     |     |
| ----------- | --- | --- |
| Scene       |     |     |
| Label       |     |     |
| Artist      |     |     |
| Incarnation |     |     |
| Album       |     |     |
| Format      |     |     |
