gfx modify spectrum default clear overwrite_colour;
gfx modify spectrum default linear range 0 0.15 extend_above white_to_red colour_range 0 1 component 1;
gfx modify spectrum default linear reverse range -0.15 0 extend_below white_to_blue colour_range 0 1 component 1;
gfx create material black normal_mode ambient 0 0 0 diffuse 0 0 0 emission 0 0 0 specular 0.3 0.3 0.3 alpha 1 shininess 0.2;
gfx create material blue normal_mode ambient 0 0 0.5 diffuse 0 0 1 emission 0 0 0 specular 0.2 0.2 0.2 alpha 1 shininess 0.2;
gfx create material bone normal_mode ambient 0.7 0.7 0.6 diffuse 0.9 0.9 0.7 emission 0 0 0 specular 0.1 0.1 0.1 alpha 1 shininess 0.2;
gfx create material default normal_mode ambient 1 1 1 diffuse 1 1 1 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create material default_selected normal_mode ambient 1 0.2 0 diffuse 1 0.2 0 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create material gold normal_mode ambient 1 0.4 0 diffuse 1 0.7 0 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3;
gfx create material gray50 normal_mode ambient 0.5 0.5 0.5 diffuse 0.5 0.5 0.5 emission 0.5 0.5 0.5 specular 0.5 0.5 0.5 alpha 1 shininess 0.2;
gfx create material green normal_mode ambient 0 0.5 0 diffuse 0 1 0 emission 0 0 0 specular 0.2 0.2 0.2 alpha 1 shininess 0.1;
gfx create material muscle normal_mode ambient 0.4 0.14 0.11 diffuse 0.5 0.12 0.1 emission 0 0 0 specular 0.3 0.5 0.5 alpha 1 shininess 0.2;
gfx create material red normal_mode ambient 0.5 0 0 diffuse 1 0 0 emission 0 0 0 specular 0.2 0.2 0.2 alpha 1 shininess 0.2;
gfx create material silver normal_mode ambient 0.4 0.4 0.4 diffuse 0.7 0.7 0.7 emission 0 0 0 specular 0.5 0.5 0.5 alpha 1 shininess 0.3;
gfx create material tissue normal_mode ambient 0.9 0.7 0.5 diffuse 0.9 0.7 0.5 emission 0 0 0 specular 0.2 0.2 0.3 alpha 1 shininess 0.2;
gfx create material transparent_gray50 normal_mode ambient 0.5 0.5 0.5 diffuse 0.5 0.5 0.5 emission 0.5 0.5 0.5 specular 0.5 0.5 0.5 alpha 0 shininess 0.2;
gfx create material white normal_mode ambient 1 1 1 diffuse 1 1 1 emission 0 0 0 specular 0 0 0 alpha 1 shininess 0;
gfx create spectrum error_spectrum;
gfx modify spectrum error_spectrum clear overwrite_colour;
gfx modify spectrum error_spectrum linear range 0.0007865 3 extend_above extend_below white_to_red colour_range 0 1 component 1;

gfx read node OptimisedExfile/LVInflation_ED 
gfx read elem OptimisedExfile/LVInflation_ED 

gfx modify g_element LVInflation_Update general clear circle_discretization 6 default_coordinate deformed element_discretization "12*12*12" native_discretization none;
gfx modify g_element LVInflation_Update lines select_on material default selected_material default_selected;
gfx modify g_element LVInflation_Update cylinders constant_radius 0.3 select_on material muscle selected_material default_selected render_shaded;
gfx modify g_element LVInflation_Update surfaces face xi3_0 select_on material muscle selected_material default_selected render_shaded;
gfx modify g_element "/" points domain_point tessellation default_points LOCAL glyph axes_solid_colour size "20*20*20" offset 0,0,0 font default select_on material default selected_material default_selected render_shaded;

gfx read data;OptimisedExfile/Surface_epi_ED region Surface_Points_Epi ;
gfx read data;OptimisedExfile/Surface_epi_$ED  time $t region Surface_Points_Epi;
gfx modify g_element Surface_Points_Epi general clear circle_discretization 6 default_coordinate coordinates element_discretization "4*4*4" native_discretization none;
gfx modify g_element Surface_Points_Epi data_points glyph sphere general size "1*1*1" centre 0,0,0 font default select_on material blue selected_material default_selected;

gfx read data;OptimisedExfile/Surface_endo_ED region Surface_Points_Endo;
gfx read data;OptimisedExfile/Surface_endo_$ED   time $t region Surface_Points_Endo;
gfx modify g_element Surface_Points_Endo general clear circle_discretization 6 default_coordinate coordinates element_discretization "4*4*4" native_discretization none;
gfx modify g_element Surface_Points_Endo data_points glyph sphere general size "1*1*1" centre 0,0,0 font default select_on material blue selected_material default_selected;

gfx read data;OptimisedError/EndoError_ED region EndoError;
gfx def field EndoError/error_mag magnitude field error;
gfx modify g_element /EndoError/ general clear;
gfx modify g_element /EndoError/ lines domain_mesh1d coordinate coordinates tessellation temp4 LOCAL line line_base_size 0 select_on material default data error spectrum default selected_material default_selected render_shaded;
gfx modify g_element /EndoError/ points domain_datapoints coordinate coordinates tessellation default_points LOCAL glyph arrow_solid size "0.8*0.8*0.8" offset 0,0,0 font default orientation error scale_factors "1*0.5*0.5" select_on material gold data error_mag spectrum error_spectrum selected_material default_selected render_shaded;

gfx read data;OptimisedError/EpiError_ED region EpiError;
gfx def field EpiError/error_mag magnitude field error;
gfx modify g_element /EpiError/ general clear;
gfx modify g_element /EpiError/ lines domain_mesh1d coordinate coordinates tessellation temp4 LOCAL line line_base_size 0 select_on material gold selected_material default_selected render_shaded;
gfx modify g_element /EpiError/ points domain_datapoints coordinate coordinates tessellation default_points LOCAL glyph arrow_solid size "0.8*0.8*0.8" offset 0,0,0 font default orientation error scale_factors "1*0.5*0.5" select_on material gold data error_mag spectrum error_spectrum selected_material default_selected render_shaded;

gfx create window 1 double_buffer;
gfx modify window 1 image scene "/" filter default light_model default;
gfx modify window 1 image add_light default;
gfx modify window 1 layout simple ortho_axes z -y eye_spacing 0.25 width 1475 height 855;
gfx modify window 1 set current_pane 1;
gfx modify window 1 background colour 1 1 1 texture none;
gfx modify window 1 view parallel eye_point -51.6351 -224.288 -262.683 interest_point 16.3439 10.0188 3.15872 up_vector -0.980988 0.0888722 0.172521 view_angle 31.99 near_clipping_plane 88.8116 far_clipping_plane 1067.96 relative_viewport ndc_placement -1 1 2 2 viewport_coordinates 0 0 1 1;
gfx modify window 1 set transform_tool current_pane 1 std_view_angle 40 normal_lines no_antialias depth_of_field 0.0 fast_transparency blend_normal;


