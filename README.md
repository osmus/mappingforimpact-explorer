# Mapping for Impact Explorer
Interactive data viewer for Mapping for Impact campaigns

Project Overview
----------------

As a crowdsourced map of the world, OpenStreetMap has disrupted the global power dynamic of who controls and has access to geospatial data. Through grassroots initiatives and community-based programs, [OpenStreetMap US](https://openstreetmap.us/) works to improve data democracy in the United States to ensure all individuals are able to access and improve the geospatial data that decision-makers and corporations use to impact our lives.

Through Mapping for Impact, OpenStreetMap US supports organizations in civic, environmental, and social sectors to solve targeted challenges and data gaps across the US using OpenStreetMap. The organizations partnering with OpenStreetMap US are in need of free, geospatial data to better showcase the needs and gaps they are working to solve. Mapping for Impact creates and improves the availability of this data to help these organizations advocate, communicate or identify needs across a wide range of causes in the United States.

OpenStreetMap US is working with our partners to identify and close geospatial data gaps, however, these organizations often do not have the capacity to visualize the data in compelling formats.  The proposed intervention is to develop an interactive map to visualize this data. This interactive map, displaying OpenStreetMap data tailored to OpenStreetMap US's impact partners' needs, will provide impact partners such as Rising Tide Effect or KABOOM! with ready-made maps using crowdsourced open geospatial data for their advocacy needs. Partners will be able to use this map in their discussions with government agencies and policymakers to effectively show gaps in public services, priority improvement areas, and highlight their geographic impact. Additionally, partners can use this with their own stakeholders and donors to show visually communicate the community needs they are working to address.

Examples of similar maps include: [Surveillance under Surveillance](https://sunders.uber.space/en/?lat=40.73177921&lon=-73.76272202&zoom=12), [NYC Street Tree Map](https://tree-map.nycgovparks.org/)

Parameters
----------

The "minimum viable product" will consist of:

1.  A reusable executable program that:

    -   Fetches current OpenStreetMap entities that match given tags in a given geographic area (e.g. using the Overpass API)

    -   Fetches entities matching the same parameters at one or more historical dates

    -   Computes statistics on the data including:

        -   Quantity of entities

        -   Quantity of users who created or modified entities

        -   Change over time for above

    -   Writes statistics to file in a standard data format

    -   Writes entities to file in a standard geospatial data format (e.g. GeoJSON)

1.  A reusable web application that:

    -   Loads output files from (1)

    -   Displays the geographic data in an interactive web map frame

        -   Uses an attractive OpenStreetMap-based basemap 

        -   Displays entity details upon selection (e.g. in popup or sidebar)

    -   Displays statistical data in a suitable manner (e.g. table, graph)

    -   Supports toggling between display of the current and historical data, or otherwise displays the change in data over time

    -   Supports toggling between campaigns (e.g. Rising Tide Effect vs KABOOM!) 

    -   Displays information about the mapping campaign and partner organization

        -   Partner name (linking out to partner website)

        -   Partner logo

    -   Campaign description (~200 words)

    -   Displays information about OpenStreetMap US & Mapping for Impact

    -   Includes elements/buttons redirecting users to:
 
        -   "Contribute to the Map" (e.g. to OSM US Tasking Manager)

        -   Github 

    -   Conforms to modern web app standards including:

        -   [Accessibility](https://en.wikipedia.org/wiki/Web_accessibility)

        -   Cross-browser support

        -   Responsive UI for both desktop and smartphone screen sizes

        -   Both mouse+keyboard and touchscreen interaction support

1.  An instance of the program (1) and web app (2) specific to Rising Tide Effect:

    -   Entity types:

    -   Geographic area: [New York City Boundary](https://tasks-backend.openstreetmap.us/api/v2/projects/312/queries/aoi/?as_file=true)
