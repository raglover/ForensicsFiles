# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'busticket.views.home'),
    (r'^student/$', 'studentapp.views.display_student_data'),
    (r'^student/edit/(\d*)', 'studentapp.views.edit_student'),
    (r'^events/edit/(\d*)', 'busticket.views.event_form'),
    (r'^events/', 'busticket.views.events'),
    (r'^tournaments/edit/(\d*)', 'busticket.views.tournament_form'),
    (r'^tournaments/', 'busticket.views.tournaments'),
    (r'^requirements/add/(\d*)', 'busticket.views.add_requirement_form'),
    (r'^requirements/(\d*)', 'busticket.views.requirements'),
)
