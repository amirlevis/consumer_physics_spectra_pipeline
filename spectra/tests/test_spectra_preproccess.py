from unittest import TestCase
from spectra.SpectraPreProccessingStep import Log, Diff, SelectWavelengths, SubtractAvg
from spectra.PreProccessPipeline import Pipeline
import numpy as np

class TestPreProccessStep(TestCase):


    def test_preProccess_log(self):
       
        spectra = np.array([[1, 2, 3],[4, 5, 6]], dtype='float64')
        step = Log()
        log = step.transform(spectra)
        
        result = np.array([[0, 0.69314718, 1.09861229], [1.38629436,1.60943791,1.79175947]], dtype='float64')
        is_equal = np.allclose(log,result)
        self.assertEqual(is_equal , True)
    
    def test_preProccess_diff(self):
        spectra = ([[1, 2, 3], [4, 6, 9]])

        step = Diff()
        diff = step.transform(spectra)
        expected_result = [[1, 1], [2, 3]]
        is_equal = np.array_equal(diff,expected_result)

        self.assertEqual(is_equal, True)

    def test_preProccess_select_wave_length(self):
       spectra = np.array([[7, 2, 5, 4, 5], [6, 7, 8, 9, 10]])
       step = SelectWavelengths(frm=1, to=3)
       new_spectra = step.transform(spectra)

       expected_result = [[2, 5, 4], [7, 8, 9]]

       is_equal = np.array_equal(new_spectra,expected_result)
       self.assertEqual(is_equal, True)


    def test_preProccess_subtractAvg(self):
        spectra = np.array([[1, 2, 0], [4, 5, 6]])
        step = SubtractAvg()
        step.fit(spectra)

        sub = step.transform (np.array([[5, 5, 5]]))
        expected_result = np.array([2.5, 1.5, 2])
        is_equal = np.allclose(sub,expected_result)
        self.assertEqual(is_equal, True)


        expected_result = [5.0, 3.5, 6.0]
        sub = step.transform (np.array([[7.5, 7.0, 9]]))
        is_equal = np.allclose(sub,expected_result)
        self.assertEqual(is_equal, True)


class TestPreProccessPipeline(TestCase):

    
    def test_pipeline_steps_count(self):

        p = Pipeline([Log(), SelectWavelengths(120, 150)])

        expected_result = 2

        self.assertEqual(len(p.steps), expected_result)
        
    
    def test_pipeline_add_steps(self):
        
        p = Pipeline([Log(), SelectWavelengths(120, 150)])
        p.add(Diff())
        expected_result = 3

        self.assertEqual(len(p.steps), expected_result)
    
    def test_pipeline_steps(self):
        p = Pipeline([SelectWavelengths(1, 3)])
        spectra = np.array([[7, 2, 5, 4, 5], [6, 7, 8, 9, 10]])

        spectra = p.proccess(spectra)
        expected_result = np.array([[2, 5, 4], [7, 8, 9]])
        is_equal = np.array_equal(spectra, expected_result)
        self.assertEqual(is_equal, True)

        p.add(Log())
        spectra = p.proccess(spectra)
        expected_result = np.array([[[0.6931471805599453, 1.6094379124341003, 1.3862943611198906],[1.9459101490553132, 2.0794415416798357, 2.1972245773362196]]])
        is_equal = np.allclose(spectra,expected_result)
        self.assertEqual(is_equal, True)

    def test_pipeline_fitted(self):

        spectra = np.array([[1, 2, 3],[4, 5, 6]])
        p = Pipeline([Log(), SubtractAvg()])
        p.proccess(spectra)

        self.assertEqual(p.fitted, True)
