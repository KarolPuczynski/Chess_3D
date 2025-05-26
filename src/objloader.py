from OpenGL.GL import *
import os

class OBJ:
    def __init__(self, filename, swapyz=False):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.gl_list = 0
        self.materials = {}
        
        dirname = os.path.dirname(filename)
        material = None
        
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue
            
            if values[0] == 'v':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertices.append(v)
            elif values[0] == 'vn':
                v = list(map(float, values[1:4]))
                if swapyz:
                    v = v[0], v[2], v[1]
                self.normals.append(v)
            elif values[0] == 'vt':
                self.texcoords.append(list(map(float, values[1:3])))
            elif values[0] in ('usemtl', 'usemat'):
                material = values[1]
            elif values[0] == 'mtllib':
                self.load_material(os.path.join(dirname, values[1]))
            elif values[0] == 'f':
                face = []
                texcoords = []
                norms = []
                for v in values[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and w[1]:
                        texcoords.append(int(w[1]))
                    else:
                        texcoords.append(0)
                    if len(w) >= 3 and w[2]:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, texcoords, material))
        
        self.generate_gl_list()

    def load_material(self, filename):
        material = None
        try:
            for line in open(filename, "r"):
                if line.startswith('#'): continue
                values = line.split()
                if not values: continue
                
                if values[0] == 'newmtl':
                    material = values[1]
                    self.materials[material] = {
                        'ambient': [0.2, 0.2, 0.2, 1.0],
                        'diffuse': [0.8, 0.8, 0.8, 1.0],
                        'specular': [0.0, 0.0, 0.0, 1.0],
                        'shininess': 0.0
                    }
                elif material and values[0] == 'Ka':
                    self.materials[material]['ambient'] = list(map(float, values[1:4])) + [1.0]
                elif material and values[0] == 'Kd':
                    self.materials[material]['diffuse'] = list(map(float, values[1:4])) + [1.0]
                elif material and values[0] == 'Ks':
                    self.materials[material]['specular'] = list(map(float, values[1:4])) + [1.0]
                elif material and values[0] == 'Ns':
                    self.materials[material]['shininess'] = float(values[1])
        except IOError:
            pass

    def generate_gl_list(self):
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        
        for face in self.faces:
            vertices, normals, texcoords, material = face
            
            if material in self.materials:
                mat = self.materials[material]
                glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, mat['ambient'])
                glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, mat['diffuse'])
                glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, mat['specular'])
                glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, mat['shininess'])
            
            glBegin(GL_TRIANGLES)
            for i in range(len(vertices)):
                if normals[i] > 0:
                    glNormal3fv(self.normals[normals[i] - 1])
                if texcoords[i] > 0:
                    glTexCoord2fv(self.texcoords[texcoords[i] - 1])
                glVertex3fv(self.vertices[vertices[i] - 1])
            glEnd()
        
        glEndList()