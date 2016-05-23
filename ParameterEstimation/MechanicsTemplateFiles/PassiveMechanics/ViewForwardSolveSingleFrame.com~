gfx create material heart ambient 0.3 0 0.3 diffuse 1 0 0 specular 0.5 0.5 0.5 shininess 0.5;
gfx create material bluey ambient 0 0.25 0.5 diffuse 0 0.4 1 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3
gfx create material copper ambient 1 0.2 0 diffuse 0.6 0.3 0 emission 0 0 0 specular 0.7 0.7 0.5 alpha 1 shininess 0.3
gfx create material gold ambient 1 0.4 0 diffuse 1 0.7 0 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.8
gfx create material silver ambient 0.4 0.4 0.4 diffuse 0.7 0.7 0.7 emission 0 0 0 specular 0.7 0.7 0.7 alpha 1 shininess 0.6
gfx cre mat trans_purple ambient 0.4 0 0.9 diffuse 0.4 0 0.9 alpha 0.3
gfx create spectrum error_spectrum;
gfx modify spectrum error_spectrum clear overwrite_colour;
gfx modify spectrum error_spectrum linear range 0.0007865 3 extend_above extend_below white_to_red colour_range 0 1 component 1;

gfx cre win 1;
gfx mod win 1 back colour "0,0,0";
gfx create material heart ambient 0.3 0 0.3 diffuse 1 0 0 specular 0.5 0.5 0.5 shininess 0.5;

gfx read node ForwardSolveExfile/LVInflation_ED region LVModel;
gfx read elem ForwardSolveExfile/LVInflation_ED region LVModel;

gfx modify g_element LVModel general clear circle_discretization 48 default_coordinate deformed element_discretization "12*12*12" native_discretization none
gfx mod g_e LVModel surfaces exterior face xi3_0 mat muscle
gfx mod g_elem LVModel cylinders constant_radius 0.2 material muscle;

gfx read node DSWall region DSWall;
gfx read elem DSWall region DSWall;

gfx modify g_element DSWall general clear circle_discretization 48 default_coordinate coordinates element_discretization "12*12*12" native_discretization none
gfx mod g_e DSWall surfaces exterior face xi3_0 mat green
gfx mod g_elem DSWall cylinders constant_radius 0.2 material green;

gfx read data Surface_Points_Epi_ED region Surface_Points_Epi;
gfx modify g_element Surface_Points_Epi data_points glyph sphere general size "2*2*2" centre 0,0,0 font default select_on material gold selected_material default_selected;

gfx read data Surface_Points_Endo_ED region Surface_Points_Endo;
gfx modify g_element Surface_Points_Endo data_points glyph sphere general size "2*2*2" centre 0,0,0 font default select_on material gold selected_material default_selected;


