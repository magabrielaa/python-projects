class ObsTracker:
    '''                                                                             
    Class for tracking observations collected over the course                       
    of an experiment using a sliding window.                                        
                                                                                    
    Attributes:                                                                     
        name (string): the name of the experiment                                   
        num_obs (int): the number of observations recorded                          
                                                                                    
    Methods:                                                                        
        add_obs(obs): adds an observation (represented as a float)                  
           to the tracker                                                           
        get_over_mean(): returns the mean of all the values                         
           added to the tracker.  Returns None if no values                         
           have been recorded.                                                      
        get_window_range(): returns a tuple with the minimum and                    
           maximum values currently in the sliding window.  Returns                 
           None if no values have been recorded.                                    
    '''

    def __init__(self, name, window_size):
        '''                                                                         
        Initialze the tracker                                                       
                                                                                   
        Args:                                                                       
            name (string): the name of the experiment                               
            window_size (int or None): the size of the sliding
                window. The size of the window will be unbounded if
                the window_size is None.
        '''

        assert (not window_size) or (window_size > 0)

        self.name = name
        self.window_size = window_size

        if window_size is not None:
            self.tracker = []
            assert len(self.tracker) <= window_size
        else:
            self.tracker = []
 

    def add_obs(self, obs):
        '''
        Add an observation to the tracker

        Args:
            obs (float): an observation
        '''
        
        self.tracker.insert(0, obs)
        if len(self.tracker) == self.window_size:
            del self.tracker[-1]

    def get_overall_mean(self):
        '''
        Returns the mean of ALL the observations that have been
        added to the tracker.
        
        Returns: float, if at least one observation has been added.  None,
        otherwise.
        '''
        if self.tracker != []:
            count = 0 
            for _ in range(len(self.tracker)):
                count += 1
            return sum(self.tracker)/count
        else:
            return None
    

    def get_window_range(self):
       '''
       Returns the minimum and maximum value currently in the sliding
       window.

       Returns: (float, float) with the minimum and maximum value in
           the sliding window, if at least one observation has been added.
           None, otherwise.
       '''

       if self.tracker != []:
           return min(self.tracker), max(self.tracker)
       elif self.tracker == []:
           return None








def mk(tname, size, obs_to_add):
    ''' Test Helper ''' 
    t = ObsTracker(tname, size) 
    for obs in obs_to_add: 
        t.add_obs(obs) 
    return t