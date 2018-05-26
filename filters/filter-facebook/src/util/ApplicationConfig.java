/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package util;
 
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;
import java.util.Properties;
import java.util.Set;
import java.util.stream.Collectors;
import javax.inject.Singleton;
import javax.ws.rs.core.Application;
//import pe.com.claro.common.property.Constantes;
//import pe.com.claro.common.resource.exception.ProviderExceptionMapper;
 
@Singleton
@javax.ws.rs.ApplicationPath("api")
public class ApplicationConfig extends Application {

    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> resources = new java.util.HashSet<>();
        System.out.println("Entro getClasses");
        resources.add(com.wordnik.swagger.jaxrs.listing.ApiListingResource.class);
        resources.add(com.wordnik.swagger.jaxrs.listing.ApiDeclarationProvider.class);
        resources.add(com.wordnik.swagger.jaxrs.listing.ApiListingResourceJSON.class);
        resources.add(com.wordnik.swagger.jaxrs.listing.ResourceListingProvider.class);
        addRestResourceClasses(resources);
        return resources;
    }

    /*@Override
    public Map<String, Object> getProperties() {
        String nombrePropertieExterno = Constantes.PROPERTIES_EXTERNO;
        Map<String, Object> dataProperties =new HashMap<String, Object>();
        dataProperties.putAll(readProperties(nombrePropertieExterno, false));
        return dataProperties;
    }*/

    private void addRestResourceClasses(Set<Class<?>> resources) {
        resources.add(base.Principal.class);
        //resources.add(ProviderExceptionMapper.class);
    }


    private Map<String, Object> readProperties(String fileInClasspath, Boolean interno) {
        InputStream is = null;
        try {
            if (interno) {
                is = this.getClass().getClassLoader().getResourceAsStream(fileInClasspath);
            } else {
            	 //is = new FileInputStream(System.getProperty(Constantes.PROPERTIESKEY) + Constantes.NOMBRERECURSO + File.separator + fileInClasspath);
            }
            Map<String, Object> map = new HashMap<String, Object>();
            Properties properties = new Properties();
            properties.load(is);
            map.putAll(properties.entrySet().stream().collect(Collectors.toMap(e -> e.getKey().toString(), e -> e.getValue())));
            return map;
        } catch (Exception e) {
            throw new RuntimeException("No se puede leer el archivo " + fileInClasspath );
        }
    }
}