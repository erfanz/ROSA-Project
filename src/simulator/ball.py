from cmath import pi
import numpy as np
import physical_object


class RigidPointBall(physical_object.RigidPhysicalObject):
    """
    easier to model as dump points are easy to calculate for a sphere
    following the light reflection model, ignoring mass and acceleration. 
    decrease the ball radius if you want it to look real.
    """
    def update_state_upon_bump(self):
        #recall that we're here because infinitesimal intersections had occured in the
        #previous cycle. 
        for in_in in self.__latest_intersections:
            if in_in.is_infinitestimal():
                # TODO we won't have this method. just an oversimplification for now
                #bump_point expected to be a numpy array with 3 elements x, y and z
                bump_point = in_in.get_intersection_point(self.oid)
                
                center_point = np.array([self.position.x,\
                    self.position.y,self.position.z])
                
                center_to_bump_unit_vector = np.linalg.norm(bump_point - center_point)
                orientation_unit_vector = np.array(self.polar_to_cartesian(1,\
                    self.position.phi,self.position.theta))
                normal_vector = np.cross(orientation_unit_vector, \
                    center_to_bump_unit_vector)
                mirror_unit_vector = np.cross(center_to_bump_unit_vector, normal_vector)
                mirror_vector = np.dot(mirror_unit_vector, orientation_unit_vector) * \
                    mirror_unit_vector
                delta_vector = mirror_vector - orientation_unit_vector
                new_orientation_unit_vector = orientation_unit_vector + 2 * delta_vector

                # a check only to know the math works fine, otherwise being a unit
                # vector is not necessary
                if np.linalg.norm(new_orientation_unit_vector) != 1:
                    raise Exception("new orientation vector norm is " + \
                        str(np.linalg.norm(new_orientation_unit_vector)))
                
                # returning here, i.e. doing one intersection only as the point object
                # cannot bump into two objects :D
                return self.cartesian_to_polar(new_orientation_unit_vector)
                
    def polar_to_cartesian(self,r,phi_degree,theta_degree):
        x= r * np.sin(theta_degree * 2*np.pi/180) * \
            np.cos(phi_degree * 2*np.pi/180)
        y= r * np.sin(theta_degree * 2*np.pi/180) * \
            np.sin(phi_degree * 2*np.pi/180)
        z= r * np.cos(theta_degree * 2*np.pi/180)
        return [x,y,z]

    def cartesian_to_polar(self,x,y,z):
        r = np.sqrt(x*x + y*y + z*z)
        theta = np.acos(z/r) * 180/ np.pi #to degrees
        phi = np.atan2(y,x) * 180/ np.pi

        # TODO do we need to keep the quanities in position in native data types?
        return [float(r), float(phi), float(theta)]
    
    def get_required_delta_t(self) -> float:
        """returns the delta_t that this object requires to operate right.
           returns 0 if the objects declares no requirement.
        """
        return 0.1


                
